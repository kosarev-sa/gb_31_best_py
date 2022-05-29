from django.contrib import admin

# Register your models here.
from approvals.models import ApprovalStatus

admin.site.register(ApprovalStatus)