from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
EMAILCHECK = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def checkreg(self, name, email, password, confirm_password):
        errorlist = []
        count = 0
        now = datetime.now()
        if len(name)<2:
            errorlist.append('First name too short!')
            count +=1

        if len(email)<1:
            errorlist.append('Email is required!')
            count+=1
        elif not EMAILCHECK.match(email):
            errorlist.append('Please enter a valid email!')
            count+=1

        if not password==confirm_password:
            errorlist.append('Passwords are not the same!')
            count+=1
        elif len(password)<8:
            errorlist.append('Please enter a password longer than 8 characters!')
            count+=1

        if count==0:
            return True
        return errorlist

    def checklog(self, email, password):
        errorlist = []
        count = 0
        if User.objects.filter(email=email).count()<1:
            count+=1
            errorlist.append('Email incorrect')
            return errorlist
        user = User.objects.get(email=email)
        password=password.encode()
        print bcrypt.hashpw(password, bcrypt.gensalt())
        print user.password
        if bcrypt.hashpw(password, user.password.encode()) != user.password:
            count+=1
            errorlist.append('Password incorrect')

        if count == 0:
            return [True, user]
        return errorlist

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    life_style = models.CharField(max_length = 200, null = True, blank = True)
    i_am = models.CharField(max_length = 300, null = True, blank = True)
    rating = models.CharField(max_length = 100, null = True, blank = True)
    popularity = models.CharField(max_length = 200, null = True, blank= True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()
    objects = models.Manager()

class UserPlace(models.Model):
    user = models.ForeignKey(User, related_name = 'place_user')
    place_url = models.CharField(max_length = 200, default='')
    name = models.CharField(max_length = 200, default='')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
