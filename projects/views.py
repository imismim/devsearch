from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects
# Create your views here.
from django.http import JsonResponse

def projects(request):
    projects, search_query = searchProjects(request)
    idUser = request.user.profile.id if request.user.is_authenticated else None
    
    custom_range, projects = paginateProjects(request, projects, 3)
    context = {"projects": projects, 'idUser': idUser, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, "projects/projects.html", context)


def project(request, id):
    idUser = request.user.profile.id if request.user.is_authenticated else None

    project = Project.objects.get(id=id)
    
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.getVoteCount
            return redirect('project', id=project.id)
    context = {"project": project, 'idUser': idUser, 'form': form}
    return render(request, "projects/single-project.html", context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        newTags = request.POST.get('newTags').split()
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            
            for tag in newTags:
                tag = tag.strip().title()
                tag, created = Tag.objects.get_or_create(name=tag)
                print(tag.name)
                project.tags.add(tag)
            form.save_m2m()
            
            return redirect('account')

    return render(request, "projects/project-form.html", {"form": form})


@login_required(login_url='login')
def updateProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newTags = request.POST.get('newTags').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newTags:
                tag = tag.strip().title()
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    return render(request, "projects/project-form.html", {"form": form})


@login_required(login_url='login')
def deleteProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'nameObj': project.title, 'typeObj': 'project'}
    return render(request, 'delete-template.html', context)

@login_required(login_url='login')
def deleteComment(request, id):
    comment = Review.objects.get(id=id)
    if request.method == 'POST':
        project = comment.project
        comment.delete()
        project.getVoteCount

        return redirect('project', id=project.id)
    
    context = {'nameObj': comment.body[:40] + '...', 'typeObj': 'comment'}
    return render(request, 'delete-template.html', context)