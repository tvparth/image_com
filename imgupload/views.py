from django.shortcuts import render, redirect,HttpResponseRedirect
from .models import ImageModel ,Cuser
from django.contrib.auth import authenticate, login
from .forms import AdminLoginForm, SignUpForm,UserForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from PIL import Image
import io
import os


# Create your views here.
def photo_list(request):
    photos = ImageModel.objects.all()
    return render(request, 'photos.html', {'photos': photos})

# Admin Login
def admin_login(request):
    form = AdminLoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "login.html", {"form": form, "msg": msg})

# Admin Register
def register_user(request):
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "singup.html", {"form": form, "msg": msg, "success": success})

# This Is User Update/Edit
def update_user(request,id):
    fm = ""
    if request.method == 'POST':
      ur = Cuser.objects.get(pk = id)
      fm = UserForm(request.POST) 
      if fm.is_valid():
          fm.save()
      else:
          ur = Cuser.objects.get(pk= id)
          fm = UserForm(instance = ur)    
    return render(request,'user_edit.html',{'fm':fm})
    

# This User Delete
def delete_user(request, id):
    if request.method == 'POST':
        ur = Cuser.objects.get(pk=id)
        ur.delete()
        return HttpResponseRedirect('/user/')


# Image Compresser
def img_compresser(request):
    if request.method == 'POST':
        image = request.FILES['upd_image']
        # If image is larger than 1 MB, compress it
        if image.size > 1000000:
            # Open image using Pillow library
            img = Image.open(image)
            # Compress image to reduce size
            img = img.resize((img.width//2, img.height//2))
            # Create a BytesIO object to hold compressed image data
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=60)

            # Create a new  compressed image data
            image = InMemoryUploadedFile(
                buffer, None, 'compressed.jpg', 'image/jpeg', buffer.getbuffer().nbytes, None
            )

        # Save the image to a local file
        with open(os.path.join(settings.MEDIA_ROOT, image.name), 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Render a success message
        return render(request, 'photos.html')

    # Render the form for GET requests
    return render(request, 'test.html')


