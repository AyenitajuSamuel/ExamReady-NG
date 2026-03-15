from django.contrib import admin
from .models import ExamSession, ExamQuestion


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 0
    readonly_fields = ("question", "order", "selected_choice", "is_correct", "answered", "answered_at")
    can_delete = False


@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display  = ("user", "exam_type", "subject", "status", "score_percent", "passed", "started_at")
    list_filter   = ("exam_type", "status", "passed", "subject")
    search_fields = ("user__username",)
    readonly_fields = ("started_at", "completed_at", "score_percent", "passed",
                       "total_questions", "correct_answers")
    inlines = [ExamQuestionInline]


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display  = ("session", "order", "question", "is_correct", "answered")
    list_filter   = ("is_correct", "answered")