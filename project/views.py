from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from account.models import *
from django.contrib import messages
from django.db.models import Q
import datetime

# Create your views here.

def staff_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    projects = Project.objects.filter(Q(company__name__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q), project_status='Pending')
    context = {'projects':projects}
    return render(request, 'home.html', context)

def customer_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    projects = Project.objects.filter(Q(company__name__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q),created_by=request.user)
    context = {'projects':projects}
    return render(request, 'home.html', context)    

@login_required
def home(request):
  if request.user.is_staff:
      return staff_view(request)
  else:
      return customer_view(request)

# def createproject(request):
#     if request.method == 'POST':
#         form = CreateprojectForm(request.POST)
#         if form.is_valid():
#             var = form.save(commit=False)
#             var.project_status = 'Pending'
#             var.save()
#             messages.info(request, 'Your project has been successfully submitted')
#             return redirect('account:dashboard')
#         else:
#             messages.warning(request,'Something went wrong')
#             return redirect('project:home')
#     else:
#         form = CreateprojectForm()
#         context = {'form':form}
#         return render(request, 'projects/clients/project_form.html',context)

def createProject(request):
    form = CreateProjectForm
    companies = Company.objects.all()
    if request.method == 'POST':
        company_name = request.POST.get('company')
        company_email = request.POST.get('company-email')
        company_contact = request.POST.get('company-contact')
        company_address = request.POST.get('company-address')
        company_city = request.POST.get('company-city')
        company,created = Company.objects.get_or_create(name=company_name,email= company_email,contact=company_contact,
                                                        address= company_address,town_city=company_city)
        
        Project.objects.create(
            company=company,
            created_by = request.user,
            title = request.POST.get('title'),
            description = request.POST.get('description'),
            project_status = 'Pending'
        )
        return redirect('project:home')


    context={'form':form,'companies':companies}
    return render(request, 'projects/clients/project_form.html', context)
    
#project detaisl
def project_detail(request,id):
    project = project.objects.get(id=id)
    project_messages = project.message_set.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            project=project,
            body=request.POST.get('body')
        )   
       # room.participants.add(request.user.name)
        return redirect('project:project-detail', id=project.id)
    t = UserBase.objects.get(user_name = project.created_by )
    projects_per_user = t.created_by.all()
    context = {'project':project, 'projects_per_user':projects_per_user,'project_messages':project_messages}
    return render(request, 'projects/clients/project_detail.html', context)

def updateProject(request,id):
    project = project.objects.get(id=id)
    form = UpdateProjectForm(instance=project)
    
    if request.method =='POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.save()
        return redirect('project:home')

    context = {'form':form, 'project':project}
    return render(request, 'projects/clients/update_project_form.html', context)

def company_details(request,id):
    project = project.objects.get(id=id)
    user = UserBase.objects.get(id=id)
    context = {'user':user,'project':project}
    return render(request, 'projects/clients/company-details.html',context)

""" For Engineers """

#view project queue
# def project_queue(request):
#     projects = project.objects.filter(project_status='Pending')
#     context = {'projects':projects}
#     return render(request, 'projects/staff/project_queue.html', context)

#accept a project from the queue
def accept_project(request,id):
    project = project.objects.get(id=id)
    project.assigned_to = request.user
    project.project_status = 'Active'
    project.accepted_date = datetime.datetime.now()
    project.save()
    messages.info(request, 'project has been accepted.Please resolve as soon as possible')
    return redirect('project:workspace')

#close a project
def close_project(request,id):
    project = project.objects.get(id=id)
    project.project_status = 'Completed'
    project.is_resolved = True
    project.closed_date = datetime.datetime.now()
    project.save()
    messages.info(request, 'project has been closed.')
    return redirect('project:home')
    
#projects engineer is working on
def workspace(request):
    projects = Project.objects.filter(assigned_to=request.user,is_resolved=False)
    company = Company.objects.all()
    context = {'projects':projects}
    return render(request, 'projects/staff/workspace.html', context)

#all closed/resolved projects
def all_closed_projects(request):
    projects = Project.objects.filter(assigned_to=request.user,is_resolved=True)
    projects.closed_date = datetime.datetime.now()
    context = {'projects':projects}
    return render(request, 'projects/staff/all_closed_projects.html', context)
            