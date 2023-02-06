from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    phones = Phone.objects.all()
    sort = request.GET.get('sort')
    if sort:
        data_sort = {
            'name': 'name',
            'min_price': 'price',
            'max_price': '-price',
                }
        phones = Phone.objects.order_by(data_sort.get(sort))
    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    print(phone.name)
    context = {'phone': phone}
    return render(request, template, context)
