from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ResumeForm, ResumeItemForm
from .models import Resume, ResumeItem


def resume_for_user(user, resume_id):
    try:
        return Resume.objects.filter(user=user).get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404


#########
# RESUMES
#########

@login_required
def resumes(request):
    """
    Handle a request to view all resumes.
    """
    resumes = Resume.objects.filter(user=request.user)\
        .order_by('name')\
        .annotate(item_count=Count('resumeitem'))

    return render(request, 'resume/resumes.html', {
        'resumes': resumes
    })


@login_required
def resume_create_view(request):
    """
    Handle a request to create a new resume.
    """
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            new_resume = form.save(commit=False)
            new_resume.user = request.user
            new_resume.save()

            return redirect(resume_edit_view, new_resume.id)
    else:
        form = ResumeForm()

    return render(request, 'resume/resume_create.html', {'form': form})


@login_required
def resume_view(request, resume_id):
    """
    Handle a request to view one resume for the user.

    :param resume_id: ID of the Resume to view.
    """
    resume = resume_for_user(request.user, resume_id)

    resume_items = ResumeItem.objects\
        .filter(resume=resume_id)\
        .order_by('-start_date')

    return render(request, 'resume/resume.html', {
        'resume': resume,
        'resume_items': resume_items
    })


@login_required
def resume_edit_view(request, resume_id):
    """
    Handle a request to edit a resume.

    :param resume_id: ID of the Resume to edit.
    """
    resume = resume_for_user(request.user, resume_id)

    template_dict = {}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume.delete()
            return redirect(resume_view)

        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            form = ResumeForm(instance=resume)
            template_dict['message'] = 'Resume updated'
    else:
        form = ResumeForm(instance=resume)

    template_dict['form'] = form

    return render(request, 'resume/resume_edit.html', template_dict)


##############
# RESUME ITEMS
##############

@login_required
def resume_item_create_view(request, resume_id):
    """
    Handle a request to create a new resume item.

    :param resume_id: ID of the Resume to add an item to.
    """
    if request.method == 'POST':
        form = ResumeItemForm(request.POST)
        if form.is_valid():
            resume = resume_for_user(request.user, resume_id)

            new_resume_item = form.save(commit=False)
            new_resume_item.resume = resume
            new_resume_item.save()

            return redirect(
                resume_item_edit_view,
                resume_id,
                new_resume_item.id
            )
    else:
        form = ResumeItemForm()

    resume = resume_for_user(request.user, resume_id)

    return render(request, 'resume/resume_item_create.html', {
        'form': form,
        'resume': resume,
    })


@login_required
def resume_item_edit_view(request, resume_id, resume_item_id):
    """
    Handle a request to edit a resume item.

    :param resume_id: ID of the Resume the ResumeItem belongs to.
    :param resume_item_id: ID of the ResumeItem to edit.
    """
    resume = resume_for_user(request.user, resume_id)

    try:
        resume_item = ResumeItem.objects\
            .filter(resume=resume_id)\
            .get(id=resume_item_id)
    except ResumeItem.DoesNotExist:
        raise Http404

    template_dict = {}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume_item.delete()
            return redirect(resume_view, resume_id)

        form = ResumeItemForm(request.POST, instance=resume_item)
        if form.is_valid():
            form.save()
            form = ResumeItemForm(instance=resume_item)
            template_dict['message'] = 'Resume item updated'
    else:
        form = ResumeItemForm(instance=resume_item)

    template_dict['form'] = form
    template_dict['resume'] = resume

    return render(request, 'resume/resume_item_edit.html', template_dict)
