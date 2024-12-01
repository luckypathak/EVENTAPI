from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import F
from events.constants import ADMIN, ERRORS, SUCCESS_MESSAGES
from events.models import Event, Ticket
from events.serializers import UserSerializer, EventSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role.lower() != ADMIN:
            return Response({"error": ERRORS["not_admin"]}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketPurchaseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        if request.user.role.lower() == ADMIN:
            return Response({"error": ERRORS["admin_ticket_purchase"]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(pk=id)
        except Event.DoesNotExist:
            return Response({"error": ERRORS["event_not_exist"]}, status=status.HTTP_400_BAD_REQUEST)

        quantity = request.data.get('quantity', 0)
        if event.tickets_sold + quantity > event.total_tickets:
            return Response({"error": ERRORS["insufficient_tickets"]}, status=status.HTTP_400_BAD_REQUEST)

        Ticket.objects.create(user=request.user, event=event, quantity=quantity)
        event.tickets_sold = F('tickets_sold') + quantity
        event.save()
        return Response({"message": SUCCESS_MESSAGES["ticket_purchase"]}, status=status.HTTP_200_OK)
