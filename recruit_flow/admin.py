from django.contrib import admin

# Register your models here.
from .models import Applicant, RecruitmentCost

admin.site.register(Applicant)
admin.site.register(RecruitmentCost)