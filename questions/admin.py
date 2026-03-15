from django.contrib import admin

from .models import Choice, Explanation, Question, Subject, Topic


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class ExplanationInline(admin.StackedInline):
    model = Explanation
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "subject", "topic", "year")
    list_filter = ("subject", "year")
    search_fields = ("question_text",)
    inlines = [ChoiceInline, ExplanationInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "subject")
    list_filter = ("subject",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("option_text", "question", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("option_text",)


@admin.register(Explanation)
class ExplanationAdmin(admin.ModelAdmin):
    list_display = ("question",)
    search_fields = ("explanation_text",)