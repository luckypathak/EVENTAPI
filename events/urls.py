from django.urls import path
from .views import RegisterView, EventView, TicketPurchaseView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:id>/purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),
]
