from django.urls import path
from .views import Index, AccountProfile, UpdateProfile
from django.shortcuts import redirect


urlpatterns = [
  path('index', Index.as_view(), name='index'),
  path('', lambda request: redirect('index', permanent=False)),
  path('accounts/profile', AccountProfile.as_view(), name='account_profile'),
  path('accounts/edit', UpdateProfile.as_view(), name='account_edit'),
]