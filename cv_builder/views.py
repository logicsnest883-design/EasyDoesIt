from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from playwright.sync_api import sync_playwright

from .models import (
    Resume, Education, Experience, Skill, Language,
    Certification, Reference, Hobby
)
from .forms import (
    ResumeForm, EducationForm, ExperienceForm, SkillForm,
    LanguageForm, CertificationForm, ReferenceForm, HobbyForm
)


TEMPLATES = [
    {'key': 'modern', 'name': 'Modern', 'desc': 'Clean sidebar layout with photo, skill bars, and teal accents. Great for tech & corporate.', 'preview': 'modern'},
    {'key': 'classic', 'name': 'Classic', 'desc': 'Traditional letterhead style, ATS-friendly. Best for law, academia, government.', 'preview': 'classic'},
    {'key': 'executive', 'name': 'Executive', 'desc': 'Bold charcoal header, centered summary. Best for senior/leadership roles.', 'preview': 'executive'},
    {'key': 'creative', 'name': 'Creative', 'desc': 'Gradient header, rounded tags, colorful timeline. Best for design & media.', 'preview': 'creative'},
    {'key': 'minimal', 'name': 'Minimal', 'desc': 'Stripped-down, content-first, fastest to scan.', 'preview': 'minimal'},
    {'key': 'compact', 'name': 'Compact', 'desc': 'Dense two-column layout to fit more on one page.', 'preview': 'compact'},
]


def user_can_access_resume(request, resume):
    if request.user.is_authenticated:
        return resume.owner_id == request.user.id

    anon_resume_ids = request.session.get('anon_resume_ids', [])
    return resume.owner_id is None and resume.pk in anon_resume_ids


def get_accessible_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)

    if not user_can_access_resume(request, resume):
        raise Http404("Resume not found.")

    return resume


def resume_list(request):
    if request.user.is_authenticated:
        resumes = Resume.objects.filter(owner=request.user).order_by('-created_at')
    else:
        anon_resume_ids = request.session.get('anon_resume_ids', [])
        resumes = Resume.objects.filter(
            owner__isnull=True,
            pk__in=anon_resume_ids
        ).order_by('-created_at')

    return render(request, 'cv_builder/resume_list.html', {'resumes': resumes})


def template_select(request):
    return render(request, 'cv_builder/template_select.html', {'templates': TEMPLATES})


def resume_create(request):
    template_key = request.GET.get('template', 'modern')

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save(commit=False)

            if request.user.is_authenticated:
                resume.owner = request.user

            resume.save()

            if not request.user.is_authenticated:
                anon_resume_ids = request.session.get('anon_resume_ids', [])

                if resume.pk not in anon_resume_ids:
                    anon_resume_ids.append(resume.pk)

                request.session['anon_resume_ids'] = anon_resume_ids
                request.session.modified = True

            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(initial={'template': template_key})

    return render(request, 'cv_builder/resume_form.html', {'form': form})


def resume_detail(request, pk):
    resume = get_accessible_resume(request, pk)

    template_map = {
        'modern': 'cv_builder/resume_detail_modern.html',
        'classic': 'cv_builder/resume_detail_classic.html',
        'creative': 'cv_builder/resume_detail_creative.html',
        'executive': 'cv_builder/resume_detail_executive.html',
        'minimal': 'cv_builder/resume_detail_minimal.html',
        'compact': 'cv_builder/resume_detail_compact.html',
    }

    template_name = template_map.get(
        resume.template,
        'cv_builder/resume_detail_modern.html'
    )

    return render(request, template_name, {'resume': resume})


@login_required
def resume_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk, owner=request.user)

    print_url_map = {
        'modern': 'resume_print_modern',
        'classic': 'resume_print_classic',
        'creative': 'resume_print_creative',
        'executive': 'resume_print_executive',
        'minimal': 'resume_print_minimal',
        'compact': 'resume_print_compact',
    }

    url_name = print_url_map.get(resume.template, 'resume_print_modern')

    print_url = request.build_absolute_uri(
        reverse(url_name, args=[resume.pk])
    )

    token = signing.dumps({
        'resume_id': resume.pk,
        'user_id': request.user.pk,
    })

    print_url = f'{print_url}?token={token}'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(print_url, wait_until='networkidle')

        pdf_bytes = page.pdf(
            format='A4',
            print_background=True,
            margin={
                'top': '0',
                'bottom': '0',
                'left': '0',
                'right': '0'
            }
        )

        browser.close()

    response = HttpResponse(
        pdf_bytes,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="{resume.full_name}_CV.pdf"'
    )

    return response


def get_print_resume(request, pk):
    token = request.GET.get('token')

    if not token:
        raise Http404("Invalid print request.")

    try:
        token_data = signing.loads(token, max_age=120)
    except (BadSignature, SignatureExpired):
        raise Http404("Print link has expired.")

    if not isinstance(token_data, dict):
        raise Http404("Invalid print request.")

    resume_id = token_data.get('resume_id')
    user_id = token_data.get('user_id')

    if str(resume_id) != str(pk):
        raise Http404("Invalid print request.")

    return get_object_or_404(Resume, pk=pk, owner_id=user_id)


def resume_print_modern(request, pk):
    resume = get_print_resume(request, pk)
    return render(request, 'cv_builder/resume_print_modern.html', {'resume': resume})


def resume_print_classic(request, pk):
    resume = get_print_resume(request, pk)
    return render(request, 'cv_builder/resume_print_classic.html', {'resume': resume})


def resume_print_creative(request, pk):
    resume = get_print_resume(request, pk)
    return render(request, 'cv_builder/resume_print_creative.html', {'resume': resume})


def resume_print_executive(request, pk):
    resume = get_print_resume(request, pk)
    return render(request, 'cv_builder/resume_print_executive.html', {'resume': resume})


def resume_print_minimal(request, pk):
    resume = get_print_resume(request, pk)
    return render(request, 'cv_builder/resume_print_minimal.html', {'resume': resume})


def resume_print_compact(request, pk):
    resume = get_print_resume(request, pk)
    return render(request, 'cv_builder/resume_print_compact.html', {'resume': resume})


def education_add(request, resume_pk):
    resume = get_accessible_resume(request, resume_pk)

    if request.method == 'POST':
        form = EducationForm(request.POST)

        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume
            education.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = EducationForm()

    return render(request, 'cv_builder/education_form.html', {
        'form': form,
        'resume': resume
    })


def education_edit(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    education = get_object_or_404(Education, pk=pk, resume=resume)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)

        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = EducationForm(instance=education)

    return render(request, 'cv_builder/education_form.html', {
        'form': form,
        'resume': resume
    })


def education_delete(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    education = get_object_or_404(Education, pk=pk, resume=resume)

    if request.method == 'POST':
        education.delete()

    return redirect('resume_detail', pk=resume.pk)


def experience_add(request, resume_pk):
    resume = get_accessible_resume(request, resume_pk)

    if request.method == 'POST':
        form = ExperienceForm(request.POST)

        if form.is_valid():
            experience = form.save(commit=False)
            experience.resume = resume
            experience.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ExperienceForm()

    return render(request, 'cv_builder/experience_form.html', {
        'form': form,
        'resume': resume
    })


def experience_edit(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    experience = get_object_or_404(Experience, pk=pk, resume=resume)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)

        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ExperienceForm(instance=experience)

    return render(request, 'cv_builder/experience_form.html', {
        'form': form,
        'resume': resume
    })


def experience_delete(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    experience = get_object_or_404(Experience, pk=pk, resume=resume)

    if request.method == 'POST':
        experience.delete()

    return redirect('resume_detail', pk=resume.pk)


def skill_add(request, resume_pk):
    resume = get_accessible_resume(request, resume_pk)

    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = SkillForm()

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Add Skill'
    })


def skill_edit(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    skill = get_object_or_404(Skill, pk=pk, resume=resume)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = SkillForm(instance=skill)

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Edit Skill'
    })


def skill_delete(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    skill = get_object_or_404(Skill, pk=pk, resume=resume)

    if request.method == 'POST':
        skill.delete()

    return redirect('resume_detail', pk=resume.pk)


def language_add(request, resume_pk):
    resume = get_accessible_resume(request, resume_pk)

    if request.method == 'POST':
        form = LanguageForm(request.POST)

        if form.is_valid():
            language = form.save(commit=False)
            language.resume = resume
            language.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = LanguageForm()

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Add Language'
    })


def language_edit(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    language = get_object_or_404(Language, pk=pk, resume=resume)

    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=language)

        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = LanguageForm(instance=language)

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Edit Language'
    })


def language_delete(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    language = get_object_or_404(Language, pk=pk, resume=resume)

    if request.method == 'POST':
        language.delete()

    return redirect('resume_detail', pk=resume.pk)


def certification_add(request, resume_pk):
    resume = get_accessible_resume(request, resume_pk)

    if request.method == 'POST':
        form = CertificationForm(request.POST)

        if form.is_valid():
            certification = form.save(commit=False)
            certification.resume = resume
            certification.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = CertificationForm()

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Add Certification'
    })


def certification_edit(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    certification = get_object_or_404(Certification, pk=pk, resume=resume)

    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)

        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = CertificationForm(instance=certification)

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Edit Certification'
    })


def certification_delete(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    certification = get_object_or_404(Certification, pk=pk, resume=resume)

    if request.method == 'POST':
        certification.delete()

    return redirect('resume_detail', pk=resume.pk)


def reference_add(request, resume_pk):
    resume = get_accessible_resume(request, resume_pk)

    if request.method == 'POST':
        form = ReferenceForm(request.POST)

        if form.is_valid():
            reference = form.save(commit=False)
            reference.resume = resume
            reference.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ReferenceForm()

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Add Reference'
    })


def reference_edit(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    reference = get_object_or_404(Reference, pk=pk, resume=resume)

    if request.method == 'POST':
        form = ReferenceForm(request.POST, instance=reference)

        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ReferenceForm(instance=reference)

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Edit Reference'
    })


def reference_delete(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    reference = get_object_or_404(Reference, pk=pk, resume=resume)

    if request.method == 'POST':
        reference.delete()

    return redirect('resume_detail', pk=resume.pk)


def hobby_add(request, resume_pk):
    resume = get_accessible_resume(request, resume_pk)

    if request.method == 'POST':
        form = HobbyForm(request.POST)

        if form.is_valid():
            hobby = form.save(commit=False)
            hobby.resume = resume
            hobby.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = HobbyForm()

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Add Hobby'
    })


def hobby_edit(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    hobby = get_object_or_404(Hobby, pk=pk, resume=resume)

    if request.method == 'POST':
        form = HobbyForm(request.POST, instance=hobby)

        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = HobbyForm(instance=hobby)

    return render(request, 'cv_builder/simple_form.html', {
        'form': form,
        'resume': resume,
        'title': 'Edit Hobby'
    })


def hobby_delete(request, resume_pk, pk):
    resume = get_accessible_resume(request, resume_pk)
    hobby = get_object_or_404(Hobby, pk=pk, resume=resume)

    if request.method == 'POST':
        hobby.delete()

    return redirect('resume_detail', pk=resume.pk)