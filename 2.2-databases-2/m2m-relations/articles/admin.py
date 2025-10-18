from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope



class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_counter = 0
        for form in self.forms:
            if len(form.cleaned_data) == 0 or form.cleaned_data.get('DELETE') == True:
                continue
            else:
                # В form.cleaned_data будет словарь с данными
                # каждой отдельной формы, которые вы можете проверить
                if form.cleaned_data['is_main'] == True:
                    is_main_counter += 1

            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if is_main_counter == 0:
            raise ValidationError('Укажите основой раздел')
        elif is_main_counter > 1:
            raise ValidationError('Основным может быть только один раздел')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 0
    fields = ['tag', 'is_main']
    can_delete = True
    formset = ScopeInlineFormset



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'text', 'published_at', 'image']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']



