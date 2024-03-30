from django.db import models
from account.models import *
from django.conf import settings
from django.urls import reverse


# Create your models here.

class Company(models.Model):
    name =  models.CharField(max_length=200)
    email =  models.CharField(max_length=400)
    contact =  models.CharField(max_length=200)
    address =  models.CharField(max_length=400)
    town_city =  models.CharField(max_length=400)
    

    class Meta:
        verbose_name_plural = 'companies'

    def get_absolute_url(self):
        return reverse('project:company-details', args=[self.id])

    def __str__(self):
        return self.name
    

class Project(models.Model):
    choices = (
        ('Active','Active'),
        ('Completed','Completed'),
        ('Pending','Pending'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='engineer',null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by',null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True,blank=True)
    closed_date = models.DateTimeField(null=True,blank=True)
    project_status = models.CharField(max_length=15,choices=choices)
    
    class Meta:
        ordering = ['-date_created']

    
    def get_absolute_url(self):
        return reverse('project:project-detail', args=[self.id])
    
    def __str__(self):
        return self.title
    
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering = ['-created', '-updated']

        def __str__(self):
            return self.body[0:50]