from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User,Listing,Bid,Comment


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required    
def new(request):
    if(request.method=="POST"):
        title = request.POST["title"]
        try:
            Listing.objects.get(title=title)
        except Listing.DoesNotExist:
            description = request.POST["description"]
            starting_bid = request.POST["starting_bid"]
            image = request.POST["image"] 
            category = request.POST["category"]
            user=request.user
            Listing.objects.create(title=title,description=description,starting_bid=starting_bid,image=image,category=category,user=user,status=True)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"auctions/new.html")

def list_view(request,list):
    if(request.method=='POST'):
      user=request.user
      listing = Listing.objects.get(id=list)
      if('comment'in request.POST):
        comment=request.POST["comment"]
        Comment.objects.create(listing=listing,comment=comment)
      if('bid' in request.POST):
        bid=request.POST["bid"]
        Bid.objects.create(listing=listing,user=user,bid=bid)
      return HttpResponseRedirect(reverse("list",args=(list,)))
    listing=Listing.objects.get(id=list)
    highest_bid = Bid.objects.filter(listing=listing).order_by("-bid").first()
    high_user = highest_bid.user == request.user.username if highest_bid else False
    return render(request,'auctions/list.html',{
        "listing":listing,
        "comments":listing.comments.all(),
        "watchlist":request.user.watchlist.all(),
        "high_user":high_user,
        "highest_bid":highest_bid,
        "myuser":request.user.username==listing.user
    })

@login_required
def close(request,list):
    listing=Listing.objects.get(id=list)
    listing.status=False
    listing.save()
    return HttpResponseRedirect(reverse("list",args=(list,)))

 
@login_required
def add(request,list_id):
    listing=Listing.objects.get(id=list_id)
    user=request.user
    user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("list",args=(list_id,)))
     
@login_required
def remove(request,list_id):
    listing=Listing.objects.get(id=list_id)
    user=request.user
    user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse('list',args=(list_id,)))
     
@login_required
def watchlist(request):
    return render(request,"auctions/watchlist.html",{
        "watchlist":request.user.watchlist.all()
    })

def categories(request):
    return render(request,"auctions/categories.html",{
        "categories":Listing.objects.values('category').distinct()
    })

def category(request,category):
    return render(request,"auctions/category.html",{
        "listing":Listing.objects.filter(category=category).all(),
        "category":category
    })