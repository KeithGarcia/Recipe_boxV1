from django import forms
from recipe_box.models import Recipe, Author

class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all(),required=False)
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=50)
    intructions = forms.CharField(widget=forms.Textarea)


class AddAuthorForm(forms.Form):
    #class Meta:
        #model = Author
        #fields=["name","bio"]
    name = forms.CharField(max_length=240)
    bio = forms.CharField(widget=forms.Textarea)
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput) 


class SignupForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class EditForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=10)
    instructions = forms.CharField(widget=forms.Textarea)       