from django import forms

from .models import ResumeItem
from .models import Resume

class ResumeItemForm(forms.ModelForm):
    """
    A form for creating and editing resume items. Note that 'user' is not
    included: it is always set to the requesting user.
    """

    class Meta:
        model = ResumeItem
        fields = ['title', 'company', 'start_date', 'end_date', 'description']


class ResumeForm(forms.ModelForm):
    """
    A form for creating and editing resume which contains resume items. Note that 'user' is not
    included: it is always set to the requesting user.
    """

    class Meta:
        model = Resume
        fields = ['name']
