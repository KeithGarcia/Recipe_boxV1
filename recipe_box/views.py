from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from recipe_box.forms import AddRecipeForm, AddAuthorForm, LoginForm, SignupForm, EditForm
from recipe_box.models import Recipe, Author


def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": my_recipes})


def recipe_detail(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    editbutton = False
    if request.user.is_staff:
        editbutton = True
    elif request.user == my_recipe.author.user:
        editbutton = True
    return render(request, "recipe_detail.html", {"recipe": my_recipe, "editbutton": editbutton})
    

def author_detail(request, author_name):
    my_author = Author.objects.get(name=author_name)
    my_recipes = Recipe.objects.all()
    isfav = False
    if request.user.is_authenticated:
        if Author.objects.filter(user=request.user, favorites=my_recipe):
            isfav = True
    return render(request, "author_detail.html", {"author": my_author, "recipes": my_recipes, "isfav": isfav})


@login_required
def add_recipe(request):
    
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            if request.user.is_staff:
                theauth= data.get('author')
            else:
                theauth = request.user.author
                      
            Recipe.objects.create(
                title=data.get('title'),
                  
                author=theauth,
                description=data.get('description'),
                time_required=data.get('time_required'),
                intructions=data.get('intructions')
                )
            return HttpResponseRedirect(reverse('homepage'))    
    if request.user.is_staff:
        the_authors= Author.objects.all()
    else: 
        the_authors = ""        
    form = AddRecipeForm()
    return render(request, "recipe_form.html", {"form": form,"authors":the_authors})


@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get("username"),password=data.get("password"))
                Author.objects.create(name=data.get("name"),bio=data.get("bio"),user=new_user)
                return HttpResponseRedirect(reverse("homepage"))

        form = AddAuthorForm()
        return render(request, "author_form.html", {"form": form})
    else:
        return HttpResponse(content=f"sorry {request.user} you do not have access to this page")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user= authenticate(request,username=data.get("username"),password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next',reverse("homepage")))
    form = LoginForm()
    return render(request,"login_form.html",{"form":form})       


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get("username"),password=data.get("password"))
            Author.objects.create(name=data.get("username"), user=new_user)
            login(request,new_user)
            return HttpResponseRedirect(reverse("homepage"))
    form = SignupForm()
    return render(request,"addauthor.html",{"form":form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


class AuthorView(TemplateView):
    def get(self, request, author_name):
        myauthor = Author.objects.get(name=author_name)
        favs = myauthor.favorites.all()
        return render(request, "author_detail.html", {"author": myauthor, "favs": favs})


class FavoriteView(TemplateView):
    def get(self, request, recipe_id):

        author = Author.objects.get(user=request.user)
        author.favorites.add(Recipe.objects.get(id=recipe_id))
        author.save()
        return HttpResponseRedirect(f'/recipe/{recipe_id}')


class EditView(TemplateView):
    def get(self, request, recipe_id):
        form = EditForm()
        return render(request, "generic_form.html", {"form": form})

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        form = EditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data.get("title")
            recipe.description = data.get("description")
            recipe.time_required = data.get("time_required")
            recipe.instructions = data.get("instructions")
            recipe.save()
            return HttpResponseRedirect(f"/recipe/{recipe_id}")



