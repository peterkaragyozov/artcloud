from django import forms

from artcloud.arts.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs= {
                    'class': 'form-control rounded-2',
                    'is_required': True,
                },
            ),
        }
