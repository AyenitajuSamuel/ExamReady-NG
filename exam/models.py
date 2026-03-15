from django.conf import settings
from django.db import models

from questions.models import Choice, Question, Subject, Topic


class ExamSession(models.Model):

    class ExamType(models.TextChoices):
        QUICK_TEST      = "quick_test",     "Quick Test"
        TIMED_EXAM      = "timed_exam",     "Timed Exam"
        PRACTICE_TOPIC  = "practice_topic", "Practice by Topic"
        WEAKNESS_DRILL  = "weakness_drill", "Weakness Drill"

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED   = "completed",   "Completed"
        ABANDONED   = "abandoned",   "Abandoned"

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exam_sessions")
    exam_type   = models.CharField(max_length=20, choices=ExamType.choices)
    subject     = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    topic       = models.ForeignKey(Topic,   on_delete=models.SET_NULL, null=True, blank=True)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    questions   = models.ManyToManyField(Question, through="ExamQuestion")

    # Timing
    duration_seconds = models.IntegerField(null=True, blank=True, help_text="Allowed time in seconds (Timed Exam only)")
    started_at       = models.DateTimeField(auto_now_add=True)
    completed_at     = models.DateTimeField(null=True, blank=True)

    # Results (populated on completion)
    total_questions  = models.IntegerField(default=0)
    correct_answers  = models.IntegerField(default=0)
    score_percent    = models.FloatField(null=True, blank=True)
    passed           = models.BooleanField(null=True, blank=True)
    pass_mark        = models.IntegerField(default=50, help_text="Pass percentage threshold")

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.username} — {self.get_exam_type_display()} ({self.started_at.date()})"

    @property
    def time_taken_seconds(self):
        if self.completed_at and self.started_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return None

    @property
    def current_question_number(self):
        return self.examquestion_set.filter(answered=True).count() + 1

    def calculate_results(self):
        exam_questions = self.examquestion_set.all()
        total   = exam_questions.count()
        correct = exam_questions.filter(is_correct=True).count()
        score   = round((correct / total) * 100, 1) if total > 0 else 0
        self.total_questions = total
        self.correct_answers = correct
        self.score_percent   = score
        self.passed          = score >= self.pass_mark
        self.save()


class ExamQuestion(models.Model):
    """Through model tracking each question's state within a session."""
    session         = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    order           = models.IntegerField()
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct      = models.BooleanField(null=True, blank=True)
    answered        = models.BooleanField(default=False)
    answered_at     = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = [("session", "question")]

    def __str__(self):
        return f"Q{self.order} in session {self.session.id}"
