from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    subastas = Listing.objects.filter(isActive=True)
    Categorias = Category.objects.all()
    return render(request, "auctions/index.html", {
        "subastas": subastas,
        "categorias": Categorias,
    })

def create(request):
    if request.method == "GET":
        Categorias = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categorias": Categorias
        })
    else:
        name = request.POST["name"]
        price = request.POST["price"]
        available = request.POST["available"]
        description = request.POST["description"]
        imgURL1 = request.POST["imgURL1"]
        imgURL2 = request.POST["imgURL2"]
        imgURL3 = request.POST["imgURL3"]
        category = request.POST["category"]
        currentUser = request.user
        categoryData = Category.objects.get(categoryType=category)
        bid = Bid(bid=int(price), user=currentUser)
        bid.save()
        newListing = Listing(
            name=name,
            price=bid,
            available=available,
            description=description,
            imgURL1=imgURL1,
            imgURL2=imgURL2,
            imgURL3=imgURL3,
            category=categoryData,
            usuario=currentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))

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

def chooseCategory(request):
    if request.method == "POST":
        categoryPick = request.POST['category']
        category = Category.objects.get(categoryType=categoryPick)
        subastas = Listing.objects.filter(isActive=True, category=category)
        Categorias = Category.objects.all()
        return render(request, "auctions/index.html", {
        "subastas": subastas,
        "categorias": Categorias,
    })

def listingDetails(request, id):
    ListingData = Listing.objects.get(pk=id)
    subastaWatchlist = request.user in ListingData.watchlist.all()
    allComments = Comment.objects.filter(subasta=ListingData)
    isOwner = request.user.username == ListingData.usuario.username
    return render(request, "auctions/detalles.html", {
        "listingDetails": ListingData,
        "subastaWatchlist": subastaWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })

def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect (reverse("detalles", args=(id, )))

def removeWatchlist (request, id):
    listingData = Listing.objects.get(pk=id) 
    currentUser = request.user 
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("detalles", args=(id, )))

def verWatchlist(request):
    currentUser = request.user
    subastas = currentUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "subastas": subastas
    })

def addBid (request,id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    subastaWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(subasta=listingData)
    isOwner = request.user.username == listingData.usuario.username 
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/detalles.html", {
            "listingDetails": listingData,
            "message": "Oferta Exitosa", 
            "update": True,
            "subastaWatchlist": subastaWatchlist,
            "isOwner": isOwner,
            "allComments": allComments
        })
    else:
        return render(request, "auctions/detalles.html", {
        "listingDetails": listingData,
        "message": "Oferta Fallida", 
        "update": False,
        "subastaWatchlist": subastaWatchlist,
        "isOwner": isOwner,
        "allComments": allComments
        })

def endAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.usuario.username
    subastaWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(subasta=listingData) 
    return render(request, "auctions/detalles.html", {
        "listingDetails": listingData,
        "subastaWatchlist": subastaWatchlist,
        "allComments": allComments,
        "update": True,
        "isOwner": isOwner,
        "message": "La subasta ha sido finalizada"
    })

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author=currentUser,
        subasta=listingData,
        message=message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("detalles", args=(id, )))