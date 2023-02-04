from django.http import HttpResponse
from django.shortcuts import render
from copy import deepcopy

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

def recipe_view(request, page):
    if page not in DATA:
        context = {}
        return render(request, 'calculator/index.html', context)
    servings = int(request.GET.get('servings', 0))
    recipe = deepcopy(DATA.get(page))
    if servings:
        for ingredient in recipe:
            recipe[ingredient] *= servings
    context = {'recipe': recipe}
    return render(request, 'calculator/index.html', context)