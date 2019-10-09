from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ResumeItemForm
from .forms import ResumeForm
from .models import ResumeItem
from .models import Resume


@login_required
def resume_view(request, resume_id):
    """
    Handle a request to view a user's resume.

    :param resume_id: The database ID of the Resume to edit.
    """
    resume_items = ResumeItem.objects\
        .filter(resume_id=resume_id) \
        .order_by('-start_date')

    try:
      resume = Resume.objects \
          .filter(user=request.user) \
          .get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404

    return render(request, 'resume/resume.html', {
        'resume_items': resume_items,
        'resume_name' : resume.name,
        'resume_id' : resume_id
    })


@login_required
def resume_list_view(request):
    """
    Handle a request to view a user's list of resumes.
    """
    resumes = Resume.objects\
        .filter(user=request.user)

    return render(request, 'resume/resume-list.html', {
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
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect(resume_view, resume.id)
    else:
        form = ResumeForm()

    return render(request, 'resume/resume_create.html', {'form': form})


@login_required
def resume_rename_view(request, resume_id):
    """
    Handle a request to rename a resume.

    :param resume_id: The database ID of the Resume to edit.
    """
    try:
        resume = Resume.objects \
            .filter(user=request.user) \
            .get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.id = resume_id
            resume.save()
            return redirect(resume_list_view)
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resume/resume_rename.html', {'form': form})

@login_required
def resume_item_create_view(request, resume_id):
    """
    Handle a request to create a new resume item.

    :param resume_id: The database ID of the Resume to edit.
    """
    try:
        resume = Resume.objects \
            .filter(user=request.user) \
            .get(id=resume_id)
    except ResumeItem.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ResumeItemForm(request.POST)
        if form.is_valid():
            new_resume_item = form.save(commit=False)
            new_resume_item.resume_id = resume_id
            new_resume_item.save()

            return redirect(resume_item_edit_view, new_resume_item.id)
    else:
        form = ResumeItemForm()

    return render(request, 'resume/resume_item_create.html', {'form': form,'resume_id':resume_id})


@login_required
def resume_item_edit_view(request, resume_item_id):
    """
    Handle a request to edit a resume item.

    :param resume_item_id: The database ID of the ResumeItem to edit.
    """
    try:
        resume_item = ResumeItem.objects\
            .get(id=resume_item_id)
    except ResumeItem.DoesNotExist:
        raise Http404

    if resume_item.resume.user != request.user:
        raise Http404

    template_dict = {}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume_item.delete()
            return redirect(resume_view, resume_item.resume.id)

        form = ResumeItemForm(request.POST, instance=resume_item)
        if form.is_valid():
            form.save()
            form = ResumeItemForm(instance=resume_item)
            template_dict['message'] = 'Resume item updated'
    else:
        form = ResumeItemForm(instance=resume_item)

    template_dict['form'] = form
    template_dict['resume_id'] = resume_item.resume_id

    return render(request, 'resume/resume_item_edit.html', template_dict)