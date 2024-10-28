from django.contrib import admin
from django.utils import timezone
import datetime

# Register your models here.

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    
    list_display =["question_text", "pub_date", "publisher", "was_published_recently"]
    
    fieldsets = [
        (None, {"fields":["question_text"]}),
        ("Date information", {"fields":["pub_date"], "classes":["collapse"]}),
        ("publisher information", {"fields":["publisher"]})
    ]
    inlines = [ChoiceInline]
    
    
    
admin.site.register(Question, QuestionAdmin)
