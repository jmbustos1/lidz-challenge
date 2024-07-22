from django.urls import path
from .views import (
    ClientListView,
    ClientDetailView,
    ClientsToDoFollowUpView,
    ClientCreateView,
    ClientScoreView,
)

urlpatterns = [
    path('clients', ClientListView.as_view(), name='client-list'),
    path('clients/<int:id>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients-to-do-follow-up/', ClientsToDoFollowUpView.as_view(), name='clients-to-do-follow-up'),
    path('clients/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:id>/score', ClientScoreView.as_view(), name='client-score'),
]