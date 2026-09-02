"""IIC-IEM – Gallery Views"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.users.decorators import admin_required
from apps.users.utils import log_activity
from apps.users.models import AdminActivityLog
from .models import Album, GalleryImage
from .forms import AlbumForm


def gallery_list(request):
    albums = Album.objects.filter(is_published=True).order_by('order_no', '-created_at')
    return render(request, 'gallery/gallery_list.html', {
        'title': 'Gallery – IIC IEM',
        'meta_description': 'Photo gallery of IIC IEM events, activities, and moments.',
        'albums': albums,
    })


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk, is_published=True)
    images = album.images.order_by('order', 'uploaded_at')
    return render(request, 'gallery/album_detail.html', {
        'title': f'{album.title} – Gallery – IIC IEM',
        'album': album,
        'images': images,
    })


@admin_required
def admin_gallery_list(request):
    albums = Album.objects.order_by('order_no', '-created_at')
    return render(request, 'gallery/admin/gallery_list.html', {'title': 'Manage Gallery', 'albums': albums})


@admin_required
def admin_album_add(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        album = form.save()
        log_activity(request.user, AdminActivityLog.ActionType.CREATE, 'Album', album.pk, album.title, request=request)
        messages.success(request, f'Album "{album.title}" created.')
        return redirect('gallery:admin_list')
    return render(request, 'gallery/admin/album_form.html', {'title': 'Add Album', 'form': form, 'action': 'Add Album'})


@admin_required
def admin_album_edit(request, pk):
    album = get_object_or_404(Album, pk=pk)
    form = AlbumForm(request.POST or None, request.FILES or None, instance=album)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Album "{album.title}" updated.')
        return redirect('gallery:admin_list')
    return render(request, 'gallery/admin/album_form.html', {'title': f'Edit: {album.title}', 'form': form, 'album': album, 'action': 'Save'})


@admin_required
@require_POST
def admin_album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    title = album.title
    album.delete()
    messages.success(request, f'Album "{title}" deleted.')
    return redirect('gallery:admin_list')


@admin_required
def admin_image_upload(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        count = 0
        for f in files:
            if f.content_type in ['image/jpeg', 'image/png', 'image/webp', 'image/gif']:
                GalleryImage.objects.create(album=album, image=f)
                count += 1
        if count:
            messages.success(request, f'{count} image(s) uploaded to "{album.title}".')
        return redirect('gallery:admin_list')
    return redirect('gallery:admin_list')


@admin_required
@require_POST
def admin_image_delete(request, img_pk):
    image = get_object_or_404(GalleryImage, pk=img_pk)
    album_pk = image.album_id
    image.image.delete(save=False)
    image.delete()
    messages.success(request, 'Image deleted.')
    return redirect('gallery:admin_list')
