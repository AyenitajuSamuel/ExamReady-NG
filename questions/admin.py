from django.contrib import admin
from .models import Question, Subject, Choice, Topic, Explanation

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Choice)
admin.site.register(Topic)
admin.site.register(Explanation)