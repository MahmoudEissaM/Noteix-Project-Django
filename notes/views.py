# notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Note, ArchivedNote, ArchiveSettings
from .forms import NoteForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.hashers import make_password, check_password

def notes_list(request):
    # This becomes the public homepage. You can show sample notes or info here.
    return render(request, 'notes/notes_list.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully!")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('dashboard')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid form data'}, status=400)
            messages.error(request, "Failed to add note. Please try again.")
    
    category = request.GET.get('category', 'All')
    if category != 'All':
        notes = Note.objects.filter(user=request.user, category=category)
    else:
        notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/dashboard.html', {'notes': notes, 'current_category': category})

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Failed to add note. Please try again.")
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('dashboard')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid form data'}, status=400)
            messages.error(request, "Failed to update note. Please try again.")
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, "Note deleted successfully!")
        return redirect('dashboard')
    # إذا لم يكن الطلب POST (مثلاً GET)، أعد توجيه المستخدم للداشبورد
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form and try again.')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def change_note_category(request, note_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            note = Note.objects.get(id=note_id, user=request.user)
            data = json.loads(request.body)
            category = data.get('category')
            if category in dict(Note.CATEGORY_CHOICES):
                note.category = category
                note.save()
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def profile(request):
    from .forms import ProfileForm, ProfileImageForm, PasswordChangeCustomForm
    user = request.user
    profile = getattr(user, 'profile', None)
    if not profile:
        from .models import Profile
        profile = Profile.objects.create(user=user)

    # Get note statistics
    total_notes = Note.objects.filter(user=user).count()
    important_notes = Note.objects.filter(user=user, category='Important').count()
    archived_notes = ArchivedNote.objects.filter(user=user).count()

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        else:
            messages.error(request, 'Failed to update profile. Please check the form.')
    else:
        profile_form = ProfileForm(instance=user)
        image_form = ProfileImageForm(instance=profile)
        password_form = PasswordChangeCustomForm(user)

    context = {
        'profile_form': profile_form,
        'image_form': image_form,
        'password_form': password_form,
        'profile': profile,
        'total_notes': total_notes,
        'important_notes': important_notes,
        'archived_notes': archived_notes,
    }
    return render(request, 'registration/profile.html', context)

@login_required
def get_note_details(request, note_id):
    try:
        note = get_object_or_404(Note, id=note_id, user=request.user)
        return JsonResponse({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'link': note.link,
            'category': note.category,
            'created_at': note.created_at.isoformat(),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def archive(request):
    # Check if PIN is configured
    settings, created = ArchiveSettings.objects.get_or_create(user=request.user)
    
    if not settings.is_configured:
        return render(request, 'notes/archive_setup.html')
        
    # Verify PIN if not already verified in session
    if not request.session.get('archive_verified'):
        return render(request, 'notes/archive_verify.html')
        
    archived_notes = ArchivedNote.objects.filter(user=request.user)
    return render(request, 'notes/archive.html', {'notes': archived_notes})

@login_required
@require_POST
def setup_archive_pin(request):
    pin_code = request.POST.get('pin_code')
    if not pin_code:
        return JsonResponse({'error': 'PIN code is required'}, status=400)
    
    settings, created = ArchiveSettings.objects.get_or_create(user=request.user)
    settings.pin_code = make_password(pin_code)
    settings.is_configured = True
    settings.save()
    
    request.session['archive_verified'] = True
    return JsonResponse({'success': True})

@login_required
@require_POST
def verify_archive_pin(request):
    pin_code = request.POST.get('pin_code')
    settings = get_object_or_404(ArchiveSettings, user=request.user)
    
    if check_password(pin_code, settings.pin_code):
        request.session['archive_verified'] = True
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid PIN'}, status=400)

@login_required
@require_POST
def move_to_archive(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    # Create archived note
    ArchivedNote.objects.create(
        user=request.user,
        title=note.title,
        content=note.content,
        original_category=note.category,
        link=note.link
    )
    
    # Delete original note
    note.delete()
    return JsonResponse({'success': True})

@login_required
@require_POST
def restore_notes(request):
    note_ids = json.loads(request.body).get('note_ids', [])
    
    if not note_ids:  # Restore all
        archived_notes = ArchivedNote.objects.filter(user=request.user)
    else:
        archived_notes = ArchivedNote.objects.filter(user=request.user, id__in=note_ids)
    
    for archived_note in archived_notes:
        Note.objects.create(
            user=request.user,
            title=archived_note.title,
            content=archived_note.content,
            category=archived_note.original_category,
            link=archived_note.link
        )
        archived_note.delete()
    
    return JsonResponse({'success': True})

@login_required
@require_POST
def delete_from_archive(request):
    note_ids = json.loads(request.body).get('note_ids', [])
    
    if not note_ids:  # Delete all
        ArchivedNote.objects.filter(user=request.user).delete()
    else:
        ArchivedNote.objects.filter(user=request.user, id__in=note_ids).delete()
    
    return JsonResponse({'success': True})

@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        from .forms import ProfileImageForm
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Process and crop/resize the image if uploaded
            if 'image' in request.FILES:
                from PIL import Image
                import os
                profile.save()  # Save first to get the file path
                img_path = profile.image.path
                img = Image.open(img_path)
                # Make the image square by cropping to the smallest dimension
                min_side = min(img.size)
                left = (img.width - min_side) // 2
                top = (img.height - min_side) // 2
                right = left + min_side
                bottom = top + min_side
                img = img.crop((left, top, right, bottom))
                # Resize to a standard size
                img = img.resize((300, 300))
                img.save(img_path)
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.error(request, 'Failed to update profile picture. Please try again.')
    return redirect('profile')
