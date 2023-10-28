from django.urls import path
from .views import allProjects, project_detail, add_comment, report_project, create_project, deleteProject,rate_project,myprojects,report_comment, edit_project,cancelProject

app_name = 'projects'


urlpatterns = [
    path("", allProjects, name="all_project"),
    path('project_detail/<int:project_id>/', project_detail, name='project_detail'),
    path('add_comment/<int:project_id>/', add_comment, name='add_comment'),
    path('<int:project_id>/report/', report_project, name='report_project'),
    path('forms/create',create_project, name='projects.create' ),
    path('forms/edit/<int:project_id>',edit_project, name='projects.edit' ),
    path('<int:id>', deleteProject,name='project.delete'),
    path('cancel_project/<int:project_id>', cancelProject,name='project.cancel'),
    path('comment/report/<int:comment_id>/', report_comment, name='report_comment'),
    path('rate_project/<int:project_id>/', rate_project, name='project.rate'),
    path("myprojects/", myprojects, name="myprojects"),
]

