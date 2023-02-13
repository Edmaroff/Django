from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        flag = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                flag += 1
        if flag == 0:
            raise ValidationError('Выберите 1 основной тег')
        elif flag > 1:
            raise ValidationError('Выберите только 1 основной тег')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # list_display = ['title', 'text', 'published_at', 'image']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['pk','name']

