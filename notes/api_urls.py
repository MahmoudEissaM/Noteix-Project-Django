from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'notes', api_views.NoteViewSet, basename='note')
router.register(r'archived-notes', api_views.ArchivedNoteViewSet, basename='archived-note')
router.register(r'profiles', api_views.ProfileViewSet, basename='profile')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('move-to-archive/<int:note_id>/', api_views.move_to_archive, name='api-move-to-archive'),
    path('restore-note/<int:archived_note_id>/', api_views.restore_note, name='api-restore-note'),
    path('setup-archive-pin/', api_views.setup_archive_pin, name='api-setup-archive-pin'),
    path('verify-archive-pin/', api_views.verify_archive_pin, name='api-verify-archive-pin'),
    path('user-profile/', api_views.user_profile, name='api-user-profile'),
    path('update-profile-pic/', api_views.update_profile_pic, name='api-update-profile-pic'),
]
