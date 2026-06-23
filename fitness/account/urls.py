from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('progress/log/', views.log_progress, name='log_progress'),

    # Premium Admin Dashboard (admin role only)
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/toggle-staff/<int:user_id>/', views.admin_toggle_staff, name='admin_toggle_staff'),
    path('admin-panel/delete-meal-plan/<int:plan_id>/', views.admin_delete_meal_plan, name='admin_delete_meal_plan'),
    path('admin-panel/delete-payment/<int:payment_id>/', views.admin_delete_payment, name='admin_delete_payment'),
    path('admin-panel/order/<int:order_id>/update-status/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin-panel/order/<int:order_id>/delete/', views.admin_delete_order, name='admin_delete_order'),
    path('admin-panel/resolve-contact/<int:contact_id>/', views.admin_resolve_contact, name='admin_resolve_contact'),
    path('admin-panel/flag-post/<int:post_id>/', views.admin_flag_post, name='admin_flag_post'),

    # Native Admin Operations
    path('admin-panel/exercise/add/', views.admin_add_exercise, name='admin_add_exercise'),
    path('admin-panel/exercise/edit/<int:id>/', views.admin_edit_exercise, name='admin_edit_exercise'),
    path('admin-panel/exercise/delete/<int:id>/', views.admin_delete_exercise, name='admin_delete_exercise'),

    path('admin-panel/blog/add/', views.admin_add_blogpost, name='admin_add_blogpost'),
    path('admin-panel/blog/edit/<int:id>/', views.admin_edit_blogpost, name='admin_edit_blogpost'),
    path('admin-panel/blog/delete/<int:id>/', views.admin_delete_blogpost, name='admin_delete_blogpost'),

    path('admin-panel/challenge/add/', views.admin_add_challenge, name='admin_add_challenge'),
    path('admin-panel/challenge/edit/<int:id>/', views.admin_edit_challenge, name='admin_edit_challenge'),
    path('admin-panel/challenge/delete/<int:id>/', views.admin_delete_challenge, name='admin_delete_challenge'),

    # Assign Plans to Users
    path('admin-panel/user/<int:user_id>/assign-exercise/', views.admin_assign_exercise, name='admin_assign_exercise'),
    path('admin-panel/user/<int:user_id>/assign-meal-plan/', views.admin_assign_meal_plan, name='admin_assign_meal_plan'),

    # Password Reset
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]

