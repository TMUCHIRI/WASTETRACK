from django.urls import path
from .views import (
    RegisterView, LoginView, VerifyOTPView,
    RequestPasswordResetView, ResetPasswordConfirmView,
    UserListView, UserUpdateRoleView,
    RegisterFCMTokenView, TestNotificationView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/password-reset/', RequestPasswordResetView.as_view(), name='password-reset-request'),
    path('auth/password-reset-confirm/', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/fcm/register/', RegisterFCMTokenView.as_view(), name='fcm-register'),
    path('auth/notifications/test/', TestNotificationView.as_view(), name='notification-test'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/role/', UserUpdateRoleView.as_view(), name='user-update-role'),
]