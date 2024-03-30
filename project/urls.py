from django.urls import path
from .import views

app_name = "project"

urlpatterns = [
    path('', views.home, name="home"),
    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<int:id>/', views.updateProject, name="update-project"),
    path('accept-project/<int:id>/', views.accept_project, name="accept-project"),   
    path('close-project/<int:id>/', views.close_project, name="close-project"),   
    path('workspace/', views.workspace, name="workspace"),   
    path('resolved projects/', views.all_closed_projects, name="all-closed"),   
    path('project-detail/<int:id>/', views.project_detail, name="project-detail"),   
    path('company-details/<int:id>/', views.company_details, name="company-details"),   
    path('all-closed-projects', views.all_closed_projects, name="all-closed-projects"),   
]