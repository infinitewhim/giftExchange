from django.urls import path
from . import views


urlpatterns = [
    path("members/", views.MemberList.as_view(), name="members"),
    path("members/<int:pk>/", views.MemberDetail.as_view(), name="members-detail"),
    path('gift-exchange/', views.GiftExchangeAPI.as_view(), name="gift-exchange"),
]
