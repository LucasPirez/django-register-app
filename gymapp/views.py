# from calendar import WEDNESDA
from django.shortcuts import redirect, render


from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseGone, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import ClassName, Questions, User, Day, Comment
from django import forms
import json
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime



class NewComment(forms.Form):
    reason = forms.CharField()
    commentary = forms.CharField(widget=forms.Textarea()) 


def index(request):

    if request.method == 'GET':
        try:
            user = User.objects.get(id= request.user.id)
            print(user.feePaid)
            userPaid = user.feePaid

        except User.DoesNotExist:
            userPaid = 0


    return render(request, 'gymapp/index.html',{
            'user': userPaid
    })


@login_required
def reserv(request):
    user = User.objects.get(id = request.user.id)
    userClass = user.stu.all()

 
    if request.method == 'POST':
        dataJson =json.loads(request.body)
        clase = ClassName.objects.get(nameClass = dataJson['clase'], classHour= dataJson['hora'])
        print(clase)
        if request.user in clase.student.all():
            clase.student.remove(request.user)
            return JsonResponse({'data': 'remove',
            'id':f"{clase.id}"})

        else:
            if len(userClass) < 2:
                clase.student.add(request.user)
                return JsonResponse({'data': 'add',
                'id':f"{clase.id}"})
            else:
                return JsonResponse({'data': 'none',
                'id':"none"})
    context = {
       
    }

    return render(request, 'gymapp/reserv.html',context)


def login_view(request):
    if request.method == "POST":
      
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

     
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "gymapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "gymapp/login.html")


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
            return render(request, "gymapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "gymapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "gymapp/register.html")

def api(request):
    objClass = ClassName.objects.all()
    if request.method == 'GET':
        objClass = objClass.order_by("classHour").all()

        return JsonResponse([obj.serialize() for obj in objClass], safe=False)
    
def comment(request,user_id):
    print(user_id)
    allComments = Comment.objects.all().order_by('-timeComment')
    value = 'no'


    if request.method == "POST":
        formComent = NewComment(request.POST)
    
        if formComent.is_valid():
            value= 'yes'
            comment = formComent.cleaned_data['commentary']
            commotive = formComent.cleaned_data['reason']
            print(request.POST)
            data = Comment()

            data.newComment = comment
            data.motive = commotive
            data.authorComment = User.objects.get(id=user_id)
            data.timeComment = datetime.now()
            data.save()

            
            return redirect('index')

    context ={
             'form': NewComment(),
            'comments':allComments,
            'value': value
        }
    return render(request, 'gymapp/comment.html',context)

def questions(request):
    quest = Questions.objects.all()

    if request.method == "POST":
        data = json.loads(request.body)
        if 'id' in data:
            com = Questions()

            com.id = data['id']
            com.quest = data['tit']
            com.answer = data['bod']

            com.save()
        else:
            com = Questions()

            com.quest = data['tit']
            com.answer = data['bod']

            com.save()

      
        print(data)
        print('hola')
    if request.method == 'PUT':
        data = json.loads(request.body)
        print(data) 
        obj = Questions.objects.get(id= data)

        

        obj.delete()


    return render(request,'gymapp/questions.html',{
        'questions':quest
    })

def enrolled(request):
    enroll = ClassName.objects.all().order_by('classHour')
    today =  datetime.now()
    
    days = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}
 
    numero_dia = int(today.strftime("%w"))
 
    day = str(days.get(numero_dia))
    print(day)
    try:
        asig = Day.objects.get(dayClass=day)
    except Day.DoesNotExist:
        asig = 0


    return render(request, 'gymapp/enrolled.html',{
        'enrolled': enroll,
        'day':asig

    })