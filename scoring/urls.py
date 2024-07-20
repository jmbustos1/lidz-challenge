from django.urls import path
from .views import ClientListView, ClientDetailView, ClientsToDoFollowUpView, ClientCreateView

urlpatterns = [
    path('clients', ClientListView.as_view(), name='client-list'),
    path('clients/<int:id>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients-to-do-follow-up/', ClientsToDoFollowUpView.as_view(), name='clients-to-do-follow-up'),
    path('client/', ClientCreateView.as_view(), name='client-create'),
]