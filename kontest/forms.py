from django import forms
from django.conf import settings
from .models import UserMasalaRelation


from django import forms
from .models import UserMasalaRelation
import uuid
import os



class UserMasalaRelationForm(forms.ModelForm):
    code = forms.CharField(
        required=False,  # Field is optional
        widget=forms.Textarea({'required': False}),
        strip=False,
    )

    def clean_code(self):
        if self.cleaned_data.get('script'):
            return
        file_name = os.path.join(settings.MEDIA_ROOT, 'scripts', str(uuid.uuid4()) + '.file')
        with open(file_name, 'w') as f:
            f.write(self.cleaned_data.get('code', ''))
        self.cleaned_data['script'] = file_name

    class Meta:
        model = UserMasalaRelation
        fields = ('language', 'script', 'code')




