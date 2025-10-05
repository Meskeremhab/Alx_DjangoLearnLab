# blog/views.py
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserUpdateForm, ProfileForm

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in after sign-up
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, instance=getattr(request.user, "profile", None))
        # ensure a profile exists
        if not hasattr(request.user, "profile"):
            from .models import Profile
            Profile.objects.create(user=request.user)
            pform = ProfileForm(request.POST, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            return redirect("profile")
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileForm(instance=getattr(request.user, "profile", None))
    return render(request, "registration/profile.html", {"uform": uform, "pform": pform})
