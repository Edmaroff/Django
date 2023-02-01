import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination import settings


def index(request):
    return redirect(reverse('bus_stations'))

with open(settings.BUS_STATION_CSV, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    CONTENT = list(reader)


def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(CONTENT, 10)
    page = paginator.get_page(page_number)
    bus_stations = list(page)
    context = {
        'bus_stations': bus_stations,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
