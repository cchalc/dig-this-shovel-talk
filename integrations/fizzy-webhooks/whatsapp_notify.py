"""
WhatsApp Notification Module

Uses Twilio API to send WhatsApp notifications for Fizzy events.
"""

from typing import Optional


class WhatsAppNotifier:
    """Send WhatsApp notifications via Twilio."""

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str,
        to_number: str
    ):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number  # Format: whatsapp:+14155238886
        self.to_number = to_number      # Format: whatsapp:+1234567890
        self._client: Optional["Client"] = None

    def _get_client(self):
        """Lazy-load Twilio client."""
        if self._client is None:
            try:
                from twilio.rest import Client
                self._client = Client(self.account_sid, self.auth_token)
            except ImportError:
                raise ImportError("twilio package required: pip install twilio")
        return self._client

    def send_message(self, body: str) -> dict:
        """Send a WhatsApp message."""
        if not self.account_sid or not self.auth_token:
            return {"success": False, "error": "Twilio credentials not configured"}

        if not self.to_number:
            return {"success": False, "error": "WhatsApp recipient not configured"}

        try:
            client = self._get_client()

            # Ensure WhatsApp format
            from_num = self.from_number if self.from_number.startswith("whatsapp:") else f"whatsapp:{self.from_number}"
            to_num = self.to_number if self.to_number.startswith("whatsapp:") else f"whatsapp:{self.to_number}"

            message = client.messages.create(
                body=body,
                from_=from_num,
                to=to_num
            )

            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_template_message(
        self,
        template_sid: str,
        content_variables: dict
    ) -> dict:
        """Send a WhatsApp template message (for approved templates)."""
        if not self.account_sid or not self.auth_token:
            return {"success": False, "error": "Twilio credentials not configured"}

        try:
            client = self._get_client()

            from_num = self.from_number if self.from_number.startswith("whatsapp:") else f"whatsapp:{self.from_number}"
            to_num = self.to_number if self.to_number.startswith("whatsapp:") else f"whatsapp:{self.to_number}"

            message = client.messages.create(
                content_sid=template_sid,
                content_variables=content_variables,
                from_=from_num,
                to=to_num
            )

            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
