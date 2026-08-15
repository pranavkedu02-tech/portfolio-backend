from datetime import datetime, timezone
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

        return Response(
            {"success": True, "detail": "Message received. Thank you!"},
            status=status.HTTP_201_CREATED,
        )