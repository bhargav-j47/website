from re import template
from traceback import print_tb
from typing_extensions import Self
from urllib.request import urlopen
from django import http
from django.shortcuts import render, redirect
from django.templatetags.static import static
from usite.models import Contact, blogposts
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login as dj_login
from  django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import *
from lxml import html
from django.conf import settings

# Create your views here. 

from usite.models import Contact



class ResponseKey():
    TITLE = 'title'
    URL = 'url'
    HEAD = 'head'
    FOOT = 'foot'
    ATTR = 'attr'
    BODY = 'body'
    NAME = 'name'
    REDIRECT = 'redirect'

fragment=['cont']

def spf_resp(content,fragments=None):
    root=html.fromstring(content)
    response = {}

    """head = html.tostring(root.get_element_by_id('head')).decode('utf-8')
    if head:
        response[ResponseKey.HEAD] = head

    foot = html.tostring(root.get_element_by_id('footer')).decode('utf-8')
    if foot:
        response[ResponseKey.FOOT] = foot"""

    """title = root.get_element_by_id('title').text
    #title=title.decode("utf-8")  
    
    

    if title:
        response[ResponseKey.TITLE] = title """

    if fragments:
        body = response[ResponseKey.BODY] = {}
        for frag_id in fragments:
            body[frag_id] =  html.tostring(root.get_element_by_id(frag_id)).decode('utf-8')
            print(html.tostring(root.get_element_by_id(frag_id)).decode('utf-8'))
            
                    
        return response


def home(request): 
    #print(request.GET.__contains__('spf'))
    if request.GET.__contains__('spf')==True:
        hc=render_to_string('index.html',request=request)
        content=spf_resp(hc,fragments=fragment)
        return JsonResponse(content)
    return render(request, 'index.html')


def contact(request):
    if request.GET.__contains__('spf')==True:
        if request.method == "POST":
            name1 = request.POST.get('name')
            email1 = request.POST.get('email')
            phone1 = request.POST.get('phone')
            desc1 = request.POST.get('desc')
            contact1 = Contact(name=name1, email=email1, phone=phone1, desc=desc1)
            contact1.save()
            messages.success(request, 'your message has been sent')
    
        contact_content=render_to_string('contact.html',request=request)
        resp=spf_resp(contact_content,fragments=fragment) 
        #return HttpResponse(JsonResponse(resp),content_type='application/json')
        return JsonResponse(resp,safe=False)
        
    else: 
        if request.method == "POST":
            name1 = request.POST.get('name')
            email1 = request.POST.get('email')
            phone1 = request.POST.get('phone')
            desc1 = request.POST.get('desc')
            contact1 = Contact(name=name1, email=email1, phone=phone1, desc=desc1)
            contact1.save()
            messages.success(request, 'your message has been sent')
        return render(request, 'contact.html')
 

    

  

def login(request):
    if request.POST.__contains__('checked'):
        settings.SESSION_COOKIE_AGE=2*7*24*60*60
    else:
        settings.SESSION_COOKIE_AGE=3600

    print(settings.SESSION_COOKIE_AGE)


    if request.user.is_authenticated:
        messages.error(request, 'already logged in with username {} logout first'.format(
            request.user.username))
        return redirect('/')
    else:

        if request.method == "POST":
            username1 = request.POST.get('username')
            password1 = request.POST.get('password')

            user = authenticate(username=username1, password=password1)

            if user is not None:
                dj_login(request, user)
                messages.success(
                    request, 'login successful welcome {}'.format(user.username))
                return redirect("/")

            else:
                messages.error(request, 'login failed try again !')
                return render(request, "login.html")     

        return render(request, "login.html")


def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'logged out successfully')
        return redirect("/")
    else:
        return redirect("/")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, password=password)

        messages.success(request, 'account created please login {}'.format(user))

        return redirect("/login")
 
    return render(request, "signup.html")

@login_required(login_url='/login')

def blog(request):
    if request.GET.__contains__('spf')==True:
        

        #blog_content='templates/blogspf.html'
        myposts=blogposts.objects.all()

        blog_content=render_to_string('blog.html',{'myposts':myposts},request=request)
        
        

        blog_resp=spf_resp(blog_content,fragments=fragment)
        #print(blog_resp)
        #data=encode_json(blog_resp)
        with open("sample.json", "w") as outfile:
            outfile.write(str(blog_resp))


         
        
    
        return JsonResponse(blog_resp,safe=False)    
        
        
    if request.method=='GET':
        if 1==1:
            """request.user.is_authenticated:"""
            myposts = blogposts.objects.all()
            return render(request, 'blog.html', {'myposts': myposts})

        else:
            messages.error(request, "you have to login to access blogs")
            return redirect('/login')


def blogpost(request):
    id=request.GET['v']
    post = blogposts.objects.filter(uuid=id)[0]
    if request.GET.__contains__('spf')==True:

        bpc=render_to_string('blogposts.html',{'post':post},request=request)

        content=spf_resp(bpc,fragments=fragment)

        return JsonResponse(content)
    return render(request, 'blogposts.html', {'post': post})


def search(request):
    print(request.GET)
    query = request.GET['query']
    if len(query) > 78:
        allPosts = blogposts.objects.none()
    else:
        allPostsTitle = blogposts.objects.filter(title__icontains=query)

        allPostsAuthor = blogposts.objects.filter(author__icontains=query)

        allPostsContent = blogposts.objects.filter(content__icontains=query)

        
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)
   
   

    if request.GET.__contains__('spf')==True:
      
        if allPosts.count() == 0:
            messages.warning(request, "No search results found. Please refine your query.")
        
        params = {'allPosts': allPosts, 'query': query}


        sc=render_to_string('search.html',params,request=request)
        content=spf_resp(sc,fragments=fragment)
        return JsonResponse(content)


    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'search.html', params)


