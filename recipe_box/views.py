from django.shortcuts import render
from recipe_box.models import Reciepe, Author
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
    return render(request,"author_detail.html",{"author":my_author,"reciepes":my_reciepes})