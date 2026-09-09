from django import forms
from .models import Students
from datetime import date


class Studentform(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )

    HOBBY_CHOICES = [
        ('art', 'Art'),
        ('coding', 'Coding'),
        ('cricket', 'Cricket'),
        ('music', 'Music'),
        ('reading', 'Reading'),
        ('gaming', 'Gaming'),
    ]

    hobbies = forms.MultipleChoiceField(
        choices=HOBBY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Students

        fields = [
            'fname',
            'sname',
            'gender',
            'dob',
            'email',
            'contact_number',
            'hobbies',
            'image',
        ]

        widgets = {
            'dob': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def clean_fname(self):
        fname = self.cleaned_data['fname'].strip()

        if not fname:
            raise forms.ValidationError(
                'First name is required.'
            )

        if not fname.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'First name should contain only letters.'
            )

        return fname

    def clean_sname(self):
        sname = self.cleaned_data['sname'].strip()

        if not sname:
            raise forms.ValidationError(
                'Last name is required.'
            )

        if not sname.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'Last name should contain only letters.'
            )

        return sname

    def clean_dob(self):
        dob = self.cleaned_data['dob']

        if dob >= date.today():
            raise forms.ValidationError(
                'Date of birth must be in the past.'
            )

        return dob

    def clean_contact_number(self):
        phone = self.cleaned_data['contact_number'].strip()

        if not phone.isdigit():
            raise forms.ValidationError(
                'Phone number should contain only digits.'
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                'Phone number must contain exactly 10 digits.'
            )

        return phone

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'Image size must be less than 5 MB.'
                )

            allowed_types = [
                'image/jpeg',
                'image/png',
                'image/jpg'
            ]

            if image.content_type not in allowed_types:
                raise forms.ValidationError(
                    'Only JPG, JPEG and PNG images are allowed.'
                )

        return image