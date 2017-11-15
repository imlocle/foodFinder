from django.shortcuts import render, redirect
from .models import User, UserPlace
import bcrypt
from django.contrib import messages
from datetime import datetime
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from django.http import JsonResponse
import json

# Create your views here.
auth = Oauth1Authenticator(
    consumer_key='QALWzkvikT2OdQXpp5u0BQ',
    consumer_secret='N96o0rgo_cAKkI2xVUX9DOTgs9A',
    token='M-0HG4VGCuLTTU-Yrz7IxZJDggdZ8wNX',
    token_secret='5XrSq-6WFQiYclv3K1mCBlVcHRw'
)

client = Client(auth)



def index(request):
    return render(request, 'wild/index.html')


def login(request):
    check = User.userManager.checklog(request.POST['loginemail'], request.POST['loginpass'])

    if check[0] == True:
        request.session['id']=check[1].id
        return redirect('/main')
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/loginreg')

def register(request):
    check = User.userManager.checkreg(request.POST['name'], request.POST['email'], request.POST['pass'], request.POST['conf_pass'])

    if check == True:
        passinput = request.POST['pass'].encode()
        hashed = bcrypt.hashpw(passinput, bcrypt.gensalt())
        the_user = User.objects.create(name=request.POST['name'], email=request.POST['email'], password=hashed)
        request.session['id'] = the_user.id
        return redirect('/preferences/'+ str(the_user.id))
    else:
        for error in check:
            messages.error(request, error)
        return redirect('/loginreg')

def loginreg(request):
    return render(request, 'wild/loginreg.html')


def main(request):
    the_user = User.objects.get(id = request.session['id'])
    if the_user:
        if 'city' in request.session:
            del request.session['city']
            del request.session['life_style']
            del request.session['rating']
            del request.session['i_am']
            del request.session['popularity']
        context = {'user': the_user}
        return render(request, 'wild/main.html', context)
    else:
        return redirect('/loginreg')

def results(request,num):
    if not 'city' in request.session:
        request.session['city'] = request.POST['city']
        request.session['life_style']=request.POST['life_style']
        request.session['rating']=request.POST['rating']
        request.session['i_am']=request.POST['i_am']
        request.session['popularity']=request.POST['popularity']
    if request.session['popularity']=='high':
        popularity = 100
    elif request.session['popularity']=='medium':
        popularity = 50
    else:
        popularity = 0

    if request.session['i_am']=='classy':
        alchohol = ',beer_and_wine'
    elif request.session['i_am']=='mess':
        alchohol = ',bars'
    else:
        alchohol = ''
    print
    params = {
        'term': 'food',
        'category_filter':request.session['life_style']+alchohol,
        'rating':request.session['rating'],
        'review_count':popularity,
    }
    response = client.search(request.session['city'], **params)
    print '**************'
    for i in range(0, 20):
        print response.businesses[i].name
        print '%%%%%%%%%%%%%%%%%%'
        print response.businesses[i].url
    print len(response.businesses)
    if int(num)==20:
        num=0
    context = {
        'response':response.businesses[int(num)],
        'num': int(num)+1,
    }
    # result = JsonResponse(response, safe=False)
    return render(request,'wild/app.html', context)

def accepted(request):
    UserPlace.objects.create(user=User.objects.get(id=request.session['id']), place_url=request.POST['url'], name=request.POST['name'])
    return redirect('/list')

def logout(request):
    del request.session['id']
    return redirect('/')

def list(request):
    joined=UserPlace.objects.filter(user=User.objects.get(id=request.session['id']))
    context = {
        'joined':joined,
    }
    return render(request, 'wild/list.html', context)

def preferences(request, id):
    return render(request, 'wild/preferences.html')

def record(request):
    the_user = User.objects.filter(id = request.session['id']).update(life_style = request.POST['life_style'], i_am = request.POST['alcohol'], rating = request.POST['rating'], popularity = request.POST['popularity'])
    return redirect('/main')

def wildrecord(request):
    the_user = User.objects.filter(id = request.session['id']).update(life_style = request.POST['life_style'], i_am = request.POST['alcohol'], rating = '1', popularity = '0')
    return redirect('/main')
