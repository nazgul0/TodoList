from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from .forms import *
from .models import *
import os


@login_required
def edit_images(request):
    if request.method == 'POST':
        edit_images_form = ImageForm(request.POST, request.FILES)
        if edit_images_form.is_valid():
            edit_images_form.save()
            messages.success(request, 'List updated successfully')
        else:
            messages.error(request, 'Error updating your list')
    else:
        edit_images_form = ImageForm(request.POST, request.FILES)
    return render(request,
                  'files/edit_images.html',
                  {'edit_images_form': edit_images_form})


@login_required
def gallery(request):
    if request.method == 'GET':
        images = Image.objects.order_by('-id').filter(user_id_id=request.user.id)
        photo = Profile.objects.get(user=request.user.id)
        underimages = UnderImage.objects.all()
        context = {
            'images': images,
            'section': 'gallery',
            'sort': 'all',
            'photo': photo,  #ава
            'underimages': underimages,
        }
        return render(request, "files/gallery.html", context)
    else:
        return render(request, "files/gallery.html")


@login_required
def oneimage(request, part):
    if request.method == 'GET':
        images = Image.objects.get(id=part)
        oneimage = UnderImage.objects.filter(image_task_id=part).order_by('-id')
        context = {
            'images': images,
            'oneimage': oneimage,
        }
        return render(request, "files/oneimage.html", context)
    else:
        return render(request, "files/oneimage.html")


@login_required
def gallery_done(request):
    if request.method == 'GET':
        images = Image.objects.order_by('-id').filter(user_id_id=request.user.id, is_done=True)
        photo = Profile.objects.get(user=request.user.id)
        context = {
            'images': images,
            'section': 'gallery',
            'sort': 'done',
            'photo': photo,
        }
        return render(request, "files/gallery.html", context)
    else:
        return render(request, "files/gallery.html")


@login_required
def gallery_todo(request):
    if request.method == 'GET':
        images = Image.objects.order_by('-id').filter(user_id_id=request.user.id, is_done=False)
        photo = Profile.objects.get(user=request.user.id)
        context = {
            'images': images,
            'section': 'gallery',
            'sort': 'todo',
            'photo': photo,
        }
        return render(request, "files/gallery.html", context)
    else:
        return render(request, "files/gallery.html")


@login_required
def upload_images(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        form.instance.user_id_id = request.user.id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = ImageForm
    context = {
        'form': form,
        'section': 'images'
    }

    return render(request, 'files/images.html', context)


@login_required
def upload_under_images(request):
    if request.method == 'POST':
        form = UnderImageForm(request.POST)
        # form.instance.user_id_id = request.user.id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UnderImageForm
    context = {
        'form': form,
        'section': 'underimages'
    }

    return render(request, 'files/underimages.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'files/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def checkTask(request):
    if request.method == "POST":
        task_id = request.POST.get('check_task_id')
        image_is_done = Image.objects.get(user_id_id=request.user.id, id=task_id)
        if image_is_done.is_done == False:
            image_is_done.is_done = True
        else:
            image_is_done.is_done = False
        image_is_done.save(update_fields=["is_done"])
        return HttpResponseRedirect("/")


@login_required
def deleteTask(request):
    if request.method == "POST":
        task_id = request.POST.get('id_task_id')
        im = Image.objects.get(user_id_id=request.user.id, id=task_id)
        os.remove(im.image.path)
        im.delete()
        return HttpResponseRedirect("/")


@login_required
def redactTask(request):
    if request.method == "GET":
        task_id = request.GET.get('red_task_id')
        print(f'------------------------------get--- {task_id} -------------------')
        si = Image.objects.get(id=task_id)
        form = ImageForm(instance=si, data=request.GET, files=request.FILES)
        context = {
            'task_id': task_id,
            'images': si,
            'form': form,
        }
        return render(request, 'files/redactTask.html', context)

    if request.method == "POST":
        task_id = request.POST.get('task_id')
        si = Image.objects.get(id=task_id)
        if len(request.FILES) != 0:
            if len(si.image) > 0:
                os.remove(si.image.path)
            si.image = request.FILES['image']
        si.title = request.POST.get('title')
        si.context = request.POST.get('context')
        si.save()
        return HttpResponseRedirect("/")


@login_required
def checkTaskUnder(request):
    if request.method == "POST":
        task_id = request.POST.get('check_task_id')
        page = request.POST.get('id_page')
        image_is_done = UnderImage.objects.get(id=task_id)
        if image_is_done.is_done == False:
            image_is_done.is_done = True
        else:
            image_is_done.is_done = False
        image_is_done.save(update_fields=["is_done"])

        task_id_image = page
        main_image_is_done = Image.objects.get(id=task_id_image)
        all_done_count = UnderImage.objects.filter(image_task_id=task_id_image, is_done=False).count()
        if all_done_count > 0:
            main_image_is_done.is_done = False
        else:
            main_image_is_done.is_done = True
        main_image_is_done.save(update_fields=["is_done"])
        return HttpResponseRedirect(f"/image/{page}")
    # task_id = request.POST.get('check_task_id')
    # image_is_done = Image.objects.get(user_id_id=request.user.id, id=task_id)
    # if image_is_done.is_done == False:
    #     image_is_done.is_done = True
    # else:
    #     image_is_done.is_done = False
    # image_is_done.save(update_fields=["is_done"])
    # return HttpResponseRedirect("/")


@login_required
def deleteTaskUnder(request):
    if request.method == "POST":
        task_id = request.POST.get('id_task_id')
        page = request.POST.get('id_page_d')
        UnderImage.objects.get(id=task_id).delete()
        return HttpResponseRedirect(f"/image/{page}")


@login_required
def redactTaskUnder(request):
    if request.method == "GET":
        task_id = request.GET.get('red_task_id')
        page = request.GET.get('page_r')
        si = UnderImage.objects.get(id=task_id)
        context = {
            'page': page,
            'images': si,
        }
        return render(request, 'files/redactTaskUnder.html', context)

    if request.method == "POST":
        task_id = request.POST.get('id_task')
        context = request.POST.get('context')
        page = request.POST.get('page')
        image_is_red = UnderImage.objects.get(id=task_id)
        image_is_red.context = context
        image_is_red.save(update_fields=["context"])
        return HttpResponseRedirect(f"/image/{page}")


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'files/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'files/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'files/register.html',
                  {'user_form': user_form})
