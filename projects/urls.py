"""
URL configuration for RaiseTogether project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import all_project, upload_multi_picture, project_detail, add_comment, report_project, create_project, deleteProject, editForm,rate_project,myprojects,report_comment, add_comment_reply

app_name = 'projects'


urlpatterns = [
    path("", all_project, name="all_project"),
    path('project_detail/<int:project_id>/', project_detail, name='project_detail'),
    path('upload/<int:project_id>/', upload_multi_picture, name='upload_multi_picture'),
    path('add_comment/<int:project_id>/', add_comment, name='add_comment'),
    path('<int:project_id>/report/', report_project, name='report_project'),
    path('forms/create',create_project, name='projects.create' ),
    path('forms/edit/<int:project_id>',editForm, name='projects.edit' ),
    path('<int:id>', deleteProject,name='project.delete'),
    path('comment/report/<int:comment_id>/', report_comment, name='report_comment'),
    path('rate_project/<int:project_id>/', rate_project, name='project.rate'),
    path("myprojects/", myprojects, name="myprojects"),
    path("add_comment_reply/<int:comment_id>/", add_comment_reply, name='add_comment_reply'),
]
