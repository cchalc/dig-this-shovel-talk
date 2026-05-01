# Fizzy Webhooks Integration

Syncs Fizzy kanban board events to GitHub Projects and sends WhatsApp notifications.

## Architecture

```
┌─────────────┐     webhook POST      ┌──────────────────┐
│   Fizzy     │ ───────────────────▶  │  Webhook Server  │
│   Board     │                       │  (Flask/Gunicorn)│
└─────────────┘                       └────────┬─────────┘
                                               │
                          ┌────────────────────┴────────────────────┐
                          ▼                                         ▼
                ┌─────────────────┐                       ┌─────────────────┐
                │  GitHub GraphQL │                       │  Twilio API     │
                │  Projects v2    │                       │  WhatsApp       │
                └─────────────────┘                       └─────────────────┘
```

## Supported Events

| Fizzy Event | GitHub Action | WhatsApp |
|-------------|---------------|----------|
| `card_closed` | Close issue, set status "Done" | Notify |
| `card_triaged` | Update project status | - |
| `card_assigned` | Add comment with assignee | Notify |
| `comment_created` | Sync comment to issue | Notify |

## Setup

### 1. Configure Environment

```bash
cd integrations/fizzy-webhooks
cp .env.example .env
# Edit .env with your credentials
```

### 2. Get Credentials

**Fizzy Signing Secret:**
1. Go to your Fizzy board
2. Click the "world" icon (top-left)
3. Create a new webhook
4. Copy the signing secret

**GitHub Token:**
1. Go to https://github.com/settings/tokens
2. Generate new token (classic) with scopes:
   - `repo` (full control)
   - `project` (full control)

**Twilio WhatsApp:**
1. Sign up at https://console.twilio.com
2. Get Account SID and Auth Token
3. Set up WhatsApp Sandbox or Business number

### 3. Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Flask dev server
python webhook_receiver.py

# Or with Gunicorn (production)
gunicorn webhook_receiver:app -b 0.0.0.0:8080
```

### 4. Expose with ngrok (for testing)

```bash
ngrok http 8080
# Copy the https URL for Fizzy webhook config
```

### 5. Configure Fizzy Webhook

1. Go to Fizzy board → "world" icon
2. Create webhook:
   - **URL:** `https://your-ngrok-url.ngrok.io/webhook/fizzy`
   - **Events:** Select all card events + comment_created
3. Save and note the signing secret

## Deployment Options

### Databricks Apps

```bash
# Create app.yaml
databricks apps create fizzy-webhooks --source-path .
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "webhook_receiver:app", "-b", "0.0.0.0:8080"]
```

### Cloud Run / Lambda

Package as container and deploy to your preferred serverless platform.

## Card Linking

For GitHub sync to work, each Fizzy card must have the GitHub issue URL in its description:

```
https://github.com/cchalc/dig-this-shovel-talk/issues/1
```

The webhook extracts the issue number from this URL.

## Testing

```bash
# Health check
curl http://localhost:8080/health

# Simulate webhook (no signature)
curl -X POST http://localhost:8080/webhook/fizzy \
  -H "Content-Type: application/json" \
  -d '{"action": "card_closed", "card": {"title": "Test", "description": "https://github.com/cchalc/dig-this-shovel-talk/issues/1"}}'
```

## Troubleshooting

**Webhook not received:**
- Check Fizzy webhook is active (auto-deactivates after 10 failures)
- Verify URL is publicly accessible
- Check ngrok/server logs

**GitHub sync fails:**
- Verify token has correct scopes
- Check issue exists in project
- Verify project number matches

**WhatsApp not sending:**
- Twilio sandbox requires opt-in: send "join <sandbox-code>" first
- Check Twilio console for error logs
