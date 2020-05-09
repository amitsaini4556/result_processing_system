from django.contrib import admin
from .models import student
from .models import department
from .models import subjects
from .models import scheme
from .models import marks
from .models import backlog
from .models import result

# models registered here so that database can be viewied in http://127.0.0.1:8000/admin/.
admin.site.register(student)
admin.site.register(department)
admin.site.register(subjects)
admin.site.register(scheme)
admin.site.register(marks)
admin.site.register(backlog)
admin.site.register(result)
