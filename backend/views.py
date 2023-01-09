import re
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import user_passes_test, login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from backend.models import *
# from backend.forms import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
# from backend.task import *
from ckeditor.fields import RichTextField
# from .decorators import *
from django.template.loader import render_to_string
import pandas as pd


import feedparser
import json
import requests
import json
import xmltodict


import urllib.request as urllib2
from bs4 import BeautifulSoup


    

def homepage(request):
    return render(request, "backend/homepage.html")


def feedparser(request):

    resp = requests.get('https://www.semrush.com/blog/feed')
  

    data_dict = xmltodict.parse(resp.content)

    json_data = json.dumps(data_dict)
    json_data = json.loads(json_data)

    new_data = {
        "item": json_data["rss"]["channel"]["item"]
    }

    return render(request, "backend/feedparser.html", new_data)


def bs4(request, page):
    print("start")
    page = int(page)
    extract_page = BeautifulSoup(urllib2.urlopen('https://www.semrush.com/blog').read(), "html.parser")
    all_list = extract_page.find("div", {"id": "articles-main"}).find("div", attrs={"data-test": "container"}).findChildren("div", recursive=False)[2].find("div", attrs={"data-test":"pagination-controls"}).find("ul", {"class": "rc-pagination"}).find_all("li")
    last_page = int(all_list[-3].find("a").text)


    soup = BeautifulSoup(urllib2.urlopen(f'https://www.semrush.com/blog?page={page}').read(), "html.parser")
    all_data = soup.find("div", {"id": "articles-main"}).find("div", attrs={"data-test": "container"}).find("div", attrs={"data-test": "columns"}).find_all("div", attrs={"data-test": "post-card-small"}) #soup.find("div", {"id": "articles-main"}).find_all("div", {"class": "sc-gsDKAQ efTgdD"})

    empty_dict = {}
    for item in range(len(all_data)):
        title = all_data[item].find("h3", attrs={"data-test": "text-content"})
        link = title.find("a").get("href")
        description = all_data[item].find("article", attrs={"data-test": "content-en"}).findChildren("div" , recursive=False)[1].find("span", attrs={"data-test": "description"}).text
        published = all_data[item].find("article", attrs={"data-test": "content-en"}).findChildren("div" , recursive=False)[1].find("div", attrs={"data-test": "meta"}).find("span", attrs={"data-test": "date"}).text 
   

        empty_dict[item] = {
            "title": title.text,
            "link": link,
            "description": description,
            "published": published
        }

    next_page = int(page) + 1
    previos_page = int(page) - 1

    params = {
        "last_page": last_page,
        "empty_dict": empty_dict,
        "current_page": page,
    }
    if (page < last_page):
        params["next_page"] = next_page

    if (page > 1):
        params["previos_page"] = previos_page
    
    print("done")
    return render(request, "backend/bs4.html", params)