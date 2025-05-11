from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),  # public home
    path('dashboard/', views.dashboard, name='dashboard'),  # user dashboard
    path('archive/', views.archive, name='archive'),
    path('setup-archive-pin/', views.setup_archive_pin, name='setup_archive_pin'),
    path('verify-archive-pin/', views.verify_archive_pin, name='verify_archive_pin'),
    path('move-to-archive/<int:note_id>/', views.move_to_archive, name='move_to_archive'),
    path('restore-notes/', views.restore_notes, name='restore_notes'),
    path('delete-from-archive/', views.delete_from_archive, name='delete_from_archive'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('update-profile-pic/', views.update_profile_pic, name='update_profile_pic'),
    path('change_category/<int:note_id>/', views.change_note_category, name='change_note_category'),
    path('api/notes/<int:note_id>/', views.get_note_details, name='note_detail_api'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/change_password.html',
        success_url='/profile/'
    ), name='change_password'),
]

