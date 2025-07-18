from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Project
from .forms import ProjectForm
# Create your views here.

def projects(request):
    projects = Project.objects.all()
    idUser = request.user.profile.id if request.user.is_authenticated else None
    return render(request, "projects/projects.html", {"projects": projects, 'idUser': idUser})

def project(request, id):
    idUser = request.user.profile.id if request.user.is_authenticated else None
    project = Project.objects.get(id=id)
    return render(request, "projects/single-project.html", {"project": project, 'idUser': idUser})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
        
    return render(request, "projects/project-form.html", {"form": form})

@login_required(login_url='login')
def updateProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
        
    return render(request, "projects/project-form.html", {"form": form})

@login_required(login_url='login')
def deleteProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id) 
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object': project}
    return render(request, 'projects/delete-project.html', context)