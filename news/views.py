from datetime import datetime
from django.shortcuts import render, redirect
from django.conf import settings
import json


# Create your views here.
def get_data_from_file():
    with open(settings.NEWS_JSON_PATH) as json_file:
        return json.load(json_file)


def coming_soon(request):
    return redirect("/news/")


def article_view(request, article_id):
    article_list = get_data_from_file()
    for article in article_list:
        if article["link"] == article_id:
            return render(request, template_name="news/article_view.html", context={"article": article})
    return redirect("/news/")


def news_view(request):
    news_list = get_data_from_file()
    for article in news_list:
        article["created"] = datetime.strptime(article["created"], "%Y-%m-%d %H:%M:%S").date()
    if request.GET.get("q") is not None:
        news_found = []
        for article in news_list:
            if article["title"] == request.GET.get("q"):
                news_found.append(article)
        news_list = news_found
    return render(request, template_name="news/index.html", context={"news_list": news_list})


def create_article(request):
    if request.method == "GET":
        return render(request, template_name="news/create_article.html")
    if request.method == "POST":
        articles_list = get_data_from_file()
        used_links = []
        for article in articles_list:
            used_links.append(int(article["link"]))
        new_link = max(used_links) + 1
        new_article = {"title": request.POST.get("title"),
                       "text": request.POST.get("text"),
                       "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       "link": new_link
                       }
        articles_list.append(new_article)
        with open(settings.NEWS_JSON_PATH, "w") as json_file:
            json.dump(articles_list, json_file)
        return redirect("/news/")
