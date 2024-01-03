from django import forms
from .models import Contact, Works


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'content', 'company', 'works']
        widgets = {
            'works': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['works'].queryset = Works.objects.all()
