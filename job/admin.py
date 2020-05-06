from django.contrib import admin
from .models import student
from .models import department
from .models import subjects
from .models import scheme
from .models import marks
from .models import backlog
from .models import result
# Register your models here.
admin.site.register(student)
admin.site.register(department)
admin.site.register(subjects)
admin.site.register(scheme)
admin.site.register(marks)
admin.site.register(backlog)
admin.site.register(result)
