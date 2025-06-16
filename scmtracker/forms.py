from django import forms
from .models import PostModeration

class PostModerationForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.HiddenInput())
    end_time = forms.TimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PostModeration
        exclude = ["moderation_date", "agent_name", "moderation_stream"]
        widgets = {
            'selected_labels': forms.SelectMultiple(attrs={'style': 'display:none;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_labels'].widget.attrs['style'] = 'display:none;'

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('agent_action')
        labels = cleaned_data.get('selected_labels')

        if action == 'rejected' and labels and len(labels) > 1:
            raise forms.ValidationError("You can only select one reason for rejection.")
        return cleaned_data
