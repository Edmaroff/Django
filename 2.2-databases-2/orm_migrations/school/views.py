from django.views.generic import ListView
from django.shortcuts import render
from .models import Student



def students_list(request):
    # 6 SQL-запросов
    # object_list = Student.objects.all()

    # 4 SQL-запроса
    object_list = Student.objects.all().prefetch_related('teachers')

    context = {'object_list': object_list}
    template = 'school/students_list.html'
    return render(request, template, context)
