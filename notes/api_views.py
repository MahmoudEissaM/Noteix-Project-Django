from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Note, ArchivedNote, Profile, ArchiveSettings
from .serializers import (
    UserSerializer, 
    NoteSerializer, 
    ArchivedNoteSerializer, 
    ProfileSerializer, 
    ArchiveSettingsSerializer
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False

class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view returns a list of all notes for the currently authenticated user.
        Optionally filtered by category.
        """
        user = self.request.user
        category = self.request.query_params.get('category', None)
        
        if category and category != 'All':
            return Note.objects.filter(user=user, category=category)
        return Note.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ArchivedNoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows archived notes to be viewed or edited.
    """
    serializer_class = ArchivedNoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view returns a list of all archived notes for the currently authenticated user.
        """
        user = self.request.user
        return ArchivedNote.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view returns the profile of the currently authenticated user.
        """
        user = self.request.user
        return Profile.objects.filter(user=user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def move_to_archive(request, note_id):
    """
    Move a note to the archive.
    """
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    # Create archived note
    archived_note = ArchivedNote.objects.create(
        user=request.user,
        title=note.title,
        content=note.content,
        original_category=note.category,
        link=note.link
    )
    
    # Delete original note
    note.delete()
    
    serializer = ArchivedNoteSerializer(archived_note)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restore_note(request, archived_note_id):
    """
    Restore a note from the archive.
    """
    archived_note = get_object_or_404(ArchivedNote, id=archived_note_id, user=request.user)
    
    # Create new note
    note = Note.objects.create(
        user=request.user,
        title=archived_note.title,
        content=archived_note.content,
        category=archived_note.original_category,
        link=archived_note.link
    )
    
    # Delete archived note
    archived_note.delete()
    
    serializer = NoteSerializer(note)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_archive_pin(request):
    """
    Setup PIN for archive access.
    """
    pin_code = request.data.get('pin_code')
    if not pin_code:
        return Response({'error': 'PIN code is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    settings, created = ArchiveSettings.objects.get_or_create(user=request.user)
    settings.pin_code = make_password(pin_code)
    settings.is_configured = True
    settings.save()
    
    serializer = ArchiveSettingsSerializer(settings)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_archive_pin(request):
    """
    Verify PIN for archive access.
    """
    pin_code = request.data.get('pin_code')
    if not pin_code:
        return Response({'error': 'PIN code is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    settings = get_object_or_404(ArchiveSettings, user=request.user)
    
    if check_password(pin_code, settings.pin_code):
        return Response({'success': True}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid PIN code'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get user profile information.
    """
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Get note statistics
    total_notes = Note.objects.filter(user=user).count()
    important_notes = Note.objects.filter(user=user, category='Important').count()
    archived_notes = ArchivedNote.objects.filter(user=user).count()
    
    user_serializer = UserSerializer(user)
    profile_serializer = ProfileSerializer(profile)
    
    return Response({
        'user': user_serializer.data,
        'profile': profile_serializer.data,
        'stats': {
            'total_notes': total_notes,
            'important_notes': important_notes,
            'archived_notes': archived_notes,
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_pic(request):
    """
    Update user profile picture.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    profile.image = request.FILES['image']
    profile.save()
    
    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)
