from django.urls import path
from user.views import *
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    # path('sign-in/', sign_in, name="sign-in"),
    path('sign-in/', CustomLoginView.as_view(), name="sign-in"),
    # path('sign-out/', sign_out, name="sign-out"),
    path('sign-out/', LogoutView.as_view(), name="sign-out"),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
    path('admin/create-group', create_group, name="create-group"),
    path('admin/group-list', group_list, name="group-list"),
    path('profile/', ProfileView.as_view(), name="user-profile"),
    path('passwd-change/', ChangePassword.as_view(template_name = 'accounts/password_change.html'), name="passwd-change"),
    path('passwd-change-done/', PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'), name="password_change_done"),
    path('passwd-reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('passwd-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]