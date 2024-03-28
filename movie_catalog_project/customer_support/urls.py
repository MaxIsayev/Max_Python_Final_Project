from django.urls import path
from . import views

urlpatterns = [
     path('new/', views.TicketCreateView.as_view(), name='ticket_create'),
     path('tickets/', views.TicketList.as_view(), name='ticket_list'),
     path('ticket/<int:pk>/', views.TicketDetail.as_view(), name='ticket_detail'),
]
