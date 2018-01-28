from django.contrib import admin

# Register your models here.
from quiz.models import *

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Question_Correct_Answer)