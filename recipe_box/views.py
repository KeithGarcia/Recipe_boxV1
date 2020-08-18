from django.shortcuts import render,HttpResponseRedirect, reverse,HttpResponse
from recipe_box.models import Reciepe, Author
from recipe_box.forms import AddRecipeForm, AddAuthorForm, LoginForm, SignupForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User



# Create your views here.
def index(request):
    my_reciepes = Reciepe.objects.all()
    return render(request, "index.html", {"reciepes": my_reciepes})


def reciepe_detail(request, reciepe_id):
    my_reciepe = Reciepe.objects.filter(id=reciepe_id).first()
    return render(request, "reciepe_detail.html", {"reciepe": my_reciepe})
    

def author_detail(request, author_name):
    my_author = Author.objects.get(name=author_name)
    my_reciepes = Reciepe.objects.all()
    return render(request, "author_detail.html", {"author": my_author, "reciepes": my_reciepes})



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
                      
            Reciepe.objects.create(
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
    return render(request, "reciepe_form.html", {"form": form,"authors":the_authors})

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






