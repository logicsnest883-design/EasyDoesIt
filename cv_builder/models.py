from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models


from django.db import models


class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('executive', 'Executive'),
        ('creative', 'Creative'),
        ('minimal', 'Minimal'),
        ('compact', 'Compact'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes', null=True, blank=True)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='modern')
    photo = models.ImageField(upload_to='resume_photos/', null=True, blank=True)

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True, help_text="Professional summary")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.qualification} - {self.institution}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Skill(models.Model):
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='intermediate')

    def __str__(self):
        return self.name


class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True)
    date_awarded = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Reference(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name



class Language(models.Model):
    PROFICIENCY_CHOICES = [
        ('basic', 'Basic'),
        ('conversational', 'Conversational'),
        ('fluent', 'Fluent'),
        ('native', 'Native'),
    ]
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='conversational')

    def __str__(self):
        return self.name


class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True)
    date_awarded = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date_awarded']

    def __str__(self):
        return self.title


class Reference(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name



class Hobby(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='hobbies')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name