from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, ArchivedNote, Profile, ArchiveSettings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']

class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'category', 'created_at', 'link']
        read_only_fields = ['user', 'created_at']

class ArchivedNoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ArchivedNote
        fields = ['id', 'user', 'title', 'content', 'original_category', 'archived_at', 'link']
        read_only_fields = ['user', 'archived_at']

class ArchiveSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ArchiveSettings
        fields = ['id', 'user', 'is_configured']
        read_only_fields = ['user']
