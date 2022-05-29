from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from users.models import User, EmployeeProfile, ModeratorProfile, EmployerProfile, Role


admin.site.register(Role)
admin.site.register(User)
admin.site.register(EmployeeProfile)
admin.site.register(EmployerProfile)
admin.site.register(ModeratorProfile)



