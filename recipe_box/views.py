from django.shortcuts import render,HttpResponseRedirect, reverse
from recipe_box.models import Reciepe, Author
from recipe_box.forms import AddRecipeForm, AddAuthorForm
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

def add_recipe(request):
    
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Reciepe.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                description=data.get('description'),
                time_required=data.get('time_required'),
                intructions=data.get('intructions')
                )
            return HttpResponseRedirect(reverse('homepage'))    
            
    form = AddRecipeForm()
    return render(request, "reciepe_form.html", {"form": form})
    
def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm()
    return render(request,"author_form.html",{"form":form})    