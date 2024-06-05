from django import forms
from core.models import Todo


class TodoForm(forms.ModelForm):
    """Form for task creation and editing."""
    class Meta:
        model = Todo
        fields = ('title', 'description', 'priority', 'complete_before',
                  'to_be_notified')


class TodoFilterForm(forms.Form):
    """Form to filter user's tasks by priority."""
    priority = forms.ChoiceField(
        choices=[('', 'All')]+Todo.PRIORITY_CHOICES,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['priority'].widget.attrs[
            'class'] = "select select-info w-full max-w-xs"
