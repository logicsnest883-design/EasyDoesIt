from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Resume, Education, Experience, Skill, Language, Certification, Reference, Hobby

admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Certification)
admin.site.register(Reference)
admin.site.register(Hobby)