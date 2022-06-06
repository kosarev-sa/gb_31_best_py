from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from users.models import User, WorkerProfile, ModeratorProfile, EmployerProfile, Role


admin.site.register(Role)
admin.site.register(User)
admin.site.register(WorkerProfile)
admin.site.register(EmployerProfile)
admin.site.register(ModeratorProfile)



