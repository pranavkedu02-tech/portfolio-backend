from datetime import datetime, timezone
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo.errors import PyMongoError
from .serializers import ContactMessageSerializer
from .db import contact_messages_collection


class ContactMessageCreateView(APIView):

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        document = serializer.validated_data
        document["created_at"] = datetime.now(timezone.utc)

        try:
            contact_messages_collection.insert_one(document)
        except PyMongoError:
            return Response(
                {"success": False, "detail": "Could not save your message right now. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self._send_thank_you_email(document["full_name"], document["email"])

        return Response(
            {"success": True, "detail": "Message received. Thank you!"},
            status=status.HTTP_201_CREATED,
        )

    def _send_thank_you_email(self, full_name, recipient_email):
        message = f"""Hi {full_name},

Thank you for visiting my portfolio and taking the time to reach out — I really appreciate it.

I've received your message and will get back to you as soon as possible, typically within a day or two.

In the meantime, feel free to explore more of my work or connect with me on LinkedIn and GitHub (linked on my portfolio).

Looking forward to connecting with you soon.

Best regards,
Pranav Khatavkar
Full Stack Developer
"""
        try:
            response = requests.post(
                "https://api.brevo.com/v3/smtp/email",
                headers={
                    "accept": "application/json",
                    "api-key": settings.BREVO_API_KEY,
                    "content-type": "application/json",
                },
                json={
                    "sender": {"name": "Pranav Khatavkar", "email": "khatavkarpranav75@gmail.com"},
                    "to": [{"email": recipient_email, "name": full_name}],
                    "subject": "Thank You for Reaching Out – Pranav Khatavkar",
                    "textContent": message,
                },
                timeout=8,
            )
            if response.status_code >= 400:
                print(f"WARNING: Brevo email failed ({response.status_code}): {response.text}")
        except requests.RequestException as e:
            print(f"WARNING: Failed to send thank-you email to {recipient_email}: {e}")