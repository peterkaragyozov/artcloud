from django import forms

from artcloud.arts.models import Art


class ArtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Art
        exclude = ('user',)
        widgets = {
            'image_url': forms.TextInput(
                attrs={
                    'id': 'img-input',
                }
            )
        }
