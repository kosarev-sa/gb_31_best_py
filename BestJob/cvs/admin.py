from django.contrib import admin

# Register your models here.
from cvs.models import CV, Education, Experience, CVSkills, LanguagesSpoken, CVEmployment, CVWorkSchedule

admin.site.register(CV)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(CVSkills)
admin.site.register(LanguagesSpoken)
admin.site.register(CVEmployment)
admin.site.register(CVWorkSchedule)