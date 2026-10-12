from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('templates/', views.template_select, name='template_select'),
    path('new/', views.resume_create, name='resume_create'),
    path('<int:pk>/', views.resume_detail, name='resume_detail'),

    path('<int:resume_pk>/education/add/', views.education_add, name='education_add'),
    path('<int:resume_pk>/education/<int:pk>/edit/', views.education_edit, name='education_edit'),
    path('<int:resume_pk>/education/<int:pk>/delete/', views.education_delete, name='education_delete'),

    path('<int:resume_pk>/experience/add/', views.experience_add, name='experience_add'),
    path('<int:resume_pk>/experience/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('<int:resume_pk>/experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
        path('<int:resume_pk>/skills/add/', views.skill_add, name='skill_add'),
    path('<int:resume_pk>/skills/<int:pk>/delete/', views.skill_delete, name='skill_delete'),

    path('<int:resume_pk>/languages/add/', views.language_add, name='language_add'),
    path('<int:resume_pk>/languages/<int:pk>/delete/', views.language_delete, name='language_delete'),

    path('<int:resume_pk>/certifications/add/', views.certification_add, name='certification_add'),
    path('<int:resume_pk>/certifications/<int:pk>/delete/', views.certification_delete, name='certification_delete'),

    path('<int:resume_pk>/references/add/', views.reference_add, name='reference_add'),
    path('<int:resume_pk>/references/<int:pk>/delete/', views.reference_delete, name='reference_delete'),
    path('<int:resume_pk>/skills/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('<int:resume_pk>/languages/<int:pk>/edit/', views.language_edit, name='language_edit'),
    path('<int:resume_pk>/certifications/<int:pk>/edit/', views.certification_edit, name='certification_edit'),
    path('<int:resume_pk>/references/<int:pk>/edit/', views.reference_edit, name='reference_edit'),
    path('<int:resume_pk>/hobbies/add/', views.hobby_add, name='hobby_add'),
    path('<int:resume_pk>/hobbies/<int:pk>/edit/', views.hobby_edit, name='hobby_edit'),
    path('<int:resume_pk>/hobbies/<int:pk>/delete/', views.hobby_delete, name='hobby_delete'),
    path('<int:pk>/pdf/', views.resume_pdf, name='resume_pdf'),
    path('<int:pk>/print/modern/', views.resume_print_modern, name='resume_print_modern'),
    path('<int:pk>/print/classic/', views.resume_print_classic, name='resume_print_classic'),
    path('<int:pk>/print/creative/', views.resume_print_creative, name='resume_print_creative'),
    path('<int:pk>/print/executive/', views.resume_print_executive, name='resume_print_executive'),
    path('<int:pk>/print/minimal/', views.resume_print_minimal, name='resume_print_minimal'),
    path('<int:pk>/print/compact/', views.resume_print_compact, name='resume_print_compact'),
]