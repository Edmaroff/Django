from django.shortcuts import render

from articles.models import Article, Tag, Scope


def articles_list(request):
    template = 'articles/news.html'
    object_list = Article.objects.all()
    context = {'object_list': object_list}
    return render(request, template, context)
