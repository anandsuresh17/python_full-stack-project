from django import forms
from .models import Students
class Studentform(forms.ModelForm):
    class Meta:
        model=Students
        fields='__all__' 

    hobbies = forms.MultipleChoiceField(
    choices=[
        ("reading", "Reading"),
        ("sports", "Sports"),
        ("music", "Music"),
        ("dance", "Dance"),
        ("painting", "Painting"),
        ("coding", "Coding"),
        ("photography", "Photography"),
        ("public_speaking", "Public Speaking"),
        ("volunteering", "Volunteering"),
        ("gaming", "Gaming"),
    ],
    widget=forms.CheckboxSelectMultiple,
    required=False
)
    class Meta:
           model=Students
           fields='__all__'