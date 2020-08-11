from django import forms
from recipe_box.models import Reciepe, Author


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=50)
    intructions = forms.CharField(widget=forms.Textarea)


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields=["name","bio"]