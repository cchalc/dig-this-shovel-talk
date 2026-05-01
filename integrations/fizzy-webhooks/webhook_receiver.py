"""
Fizzy Webhook Receiver

Receives webhooks from Fizzy and:
1. Updates GitHub Projects to keep issues in sync
2. Sends WhatsApp notifications for key events
"""

import hashlib
import hmac
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

from github_sync import GitHubProjectSync
from whatsapp_notify import WhatsAppNotifier

app = Flask(__name__)

# Configuration from environment
FIZZY_SIGNING_SECRET = os.environ.get("FIZZY_SIGNING_SECRET", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_PROJECT_ID = os.environ.get("GITHUB_PROJECT_ID", "2")  # Project number
GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "cchalc")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
WHATSAPP_TO = os.environ.get("WHATSAPP_TO", "")  # recipient number
WHATSAPP_FROM = os.environ.get("WHATSAPP_FROM", "")  # Twilio WhatsApp number

# Initialize integrations
github_sync = GitHubProjectSync(
    token=GITHUB_TOKEN,
    owner=GITHUB_OWNER,
    project_number=int(GITHUB_PROJECT_ID)
)

whatsapp = WhatsAppNotifier(
    account_sid=TWILIO_ACCOUNT_SID,
    auth_token=TWILIO_AUTH_TOKEN,
    from_number=WHATSAPP_FROM,
    to_number=WHATSAPP_TO
)

# Map Fizzy columns to GitHub Project status
COLUMN_TO_STATUS = {
    "Backlog": "Backlog",
    "Phase 1: Foundation": "In Progress",
    "Phase 2: Simulation": "Todo",
    "Phase 3: Advanced": "Todo",
    "Done": "Done"
}

# Events that trigger WhatsApp notifications
NOTIFY_EVENTS = ["card_closed", "card_assigned", "comment_created"]


def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify Fizzy webhook signature using HMAC-SHA256."""
    if not FIZZY_SIGNING_SECRET:
        app.logger.warning("No signing secret configured, skipping verification")
        return True

    expected = hmac.new(
        FIZZY_SIGNING_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


def extract_github_issue_number(card: dict) -> int | None:
    """Extract GitHub issue number from card description."""
    description = card.get("description", "") or ""
    # Look for pattern: github.com/.../issues/123
    import re
    match = re.search(r"github\.com/[^/]+/[^/]+/issues/(\d+)", description)
    if match:
        return int(match.group(1))
    return None


@app.route("/webhook/fizzy", methods=["POST"])
def handle_fizzy_webhook():
    """Handle incoming Fizzy webhook."""
    # Verify signature
    signature = request.headers.get("X-Webhook-Signature", "")
    if not verify_signature(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401

    # Parse payload
    try:
        payload = request.json
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {e}"}), 400

    event_type = payload.get("action", "unknown")
    card = payload.get("card", {})
    board = payload.get("board", {})

    app.logger.info(f"Received Fizzy webhook: {event_type}")
    app.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

    # Extract GitHub issue number from card
    issue_number = extract_github_issue_number(card)

    results = {
        "event": event_type,
        "card_title": card.get("title", ""),
        "github_issue": issue_number,
        "actions": []
    }

    # Sync to GitHub if we have an issue link
    if issue_number and GITHUB_TOKEN:
        try:
            github_result = sync_to_github(event_type, card, issue_number)
            results["actions"].append({"github": github_result})
        except Exception as e:
            app.logger.error(f"GitHub sync failed: {e}")
            results["actions"].append({"github": {"error": str(e)}})

    # Send WhatsApp notification for key events
    if event_type in NOTIFY_EVENTS and TWILIO_ACCOUNT_SID:
        try:
            notification_result = send_notification(event_type, card, board)
            results["actions"].append({"whatsapp": notification_result})
        except Exception as e:
            app.logger.error(f"WhatsApp notification failed: {e}")
            results["actions"].append({"whatsapp": {"error": str(e)}})

    return jsonify(results), 200


def sync_to_github(event_type: str, card: dict, issue_number: int) -> dict:
    """Sync Fizzy card state to GitHub Project."""
    result = {"issue": issue_number, "synced": False}

    if event_type == "card_closed":
        # Move issue to Done in project
        github_sync.update_issue_status(issue_number, "Done")
        github_sync.close_issue(issue_number)
        result["synced"] = True
        result["action"] = "closed"

    elif event_type == "card_triaged":
        # Card moved to a column - update project status
        column_name = card.get("column", {}).get("name", "")
        status = COLUMN_TO_STATUS.get(column_name, "Todo")
        github_sync.update_issue_status(issue_number, status)
        result["synced"] = True
        result["action"] = f"moved to {status}"

    elif event_type == "card_assigned":
        # Add assignee comment (can't directly assign without username mapping)
        assignee = card.get("assignee", {}).get("name", "someone")
        github_sync.add_comment(
            issue_number,
            f"Assigned to {assignee} in Fizzy"
        )
        result["synced"] = True
        result["action"] = f"assigned to {assignee}"

    elif event_type == "comment_created":
        # Sync comment to GitHub
        comment = card.get("comment", {})
        comment_body = comment.get("content", "")
        author = comment.get("creator", {}).get("name", "Someone")
        github_sync.add_comment(
            issue_number,
            f"**Comment from Fizzy ({author}):**\n\n{comment_body}"
        )
        result["synced"] = True
        result["action"] = "comment synced"

    return result


def send_notification(event_type: str, card: dict, board: dict) -> dict:
    """Send WhatsApp notification for Fizzy event."""
    card_title = card.get("title", "Unknown card")
    board_name = board.get("name", "Unknown board")

    if event_type == "card_closed":
        message = f"Task completed in {board_name}: {card_title}"
    elif event_type == "card_assigned":
        assignee = card.get("assignee", {}).get("name", "someone")
        message = f"Task assigned to {assignee}: {card_title}"
    elif event_type == "comment_created":
        author = card.get("comment", {}).get("creator", {}).get("name", "Someone")
        message = f"New comment from {author} on: {card_title}"
    else:
        message = f"Update on {board_name}: {event_type} - {card_title}"

    return whatsapp.send_message(message)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "integrations": {
            "github": bool(GITHUB_TOKEN),
            "whatsapp": bool(TWILIO_ACCOUNT_SID)
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
