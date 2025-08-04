from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db.models import Q

from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles
# Create your views here.


@never_cache
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
            messages.error(request, 'Username OR Password is not correct')

    return render(request, 'users/login-register.html', {"page": page})


def logoutUser(request):
    logout(request)
    return redirect('login')


@never_cache
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User successfully created')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(
                request, 'An error has occurred during registrations')

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context)


def profiles(request):
    idUser = request.user.profile.id if request.user.is_authenticated else None
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)

    return render(request, 'users/profiles.html', {'profiles': profiles, 'idUser': idUser, 'search_query': search_query, 'custom_range': custom_range})


def userProfile(request, id):
    profile = Profile.objects.get(id=id)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    }
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile,
               'skills': skills,
               'projects': projects, }
    return render(request, "users/account.html", context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was created successfully!')
        return redirect('account')

    context = {'form': form}
    return render(request, 'users/create-skill.html', context)


@login_required(login_url='login')
def editSkill(request, id):
    skill = request.user.profile.skill_set.get(id=id)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was update successfully!')
        return redirect('account')

    context = {'form': form}
    return render(request, 'users/create-skill.html', context)


@login_required(login_url='login')
def deleteSkill(request, id):
    skill = request.user.profile.skill_set.get(id=id)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'nameObj': skill.name, 'typeObj': 'skill'}
    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, id):
    profile = request.user.profile
    messageObj = profile.messages.get(id=id)
    messageObj.is_read = True
    messageObj.save()
    context = {'messageObj': messageObj}
    return render(request, 'users/message.html', context)


@login_required(login_url='login')
def createMessage(request, id):
    recipient = Profile.objects.get(id=id)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.recipient = recipient
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', id=recipient.id)
        
    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message-form.html', context)

@login_required(login_url='login')
def deleteMessage(request, id):
    profile = request.user.profile
    messageObj = profile.messages.get(id=id)
    if request.method == 'POST':
        messageObj.delete()
        messages.success(request, 'Message was deleted successfully!')
        return redirect('inbox')
    context = {'nameObj': messageObj.subject, 'typeObj': 'message'}
    return render(request, 'delete-template.html', context)