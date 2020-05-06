"""rps URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import job.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:error_message>/',job.views.home,name='home'),
    path('',job.views.home,name='home'),
    path('dept_form',job.views.dept_form,name='dept_form'),
    path('student_form',job.views.student_form,name='student_form'),
    path('scheme_form',job.views.scheme_form,name='scheme_form'),
    path('sub_form',job.views.sub_form,name='sub_form'),
    path('marks_form',job.views.marks_form,name='marks_form'),
    path('result_form',job.views.result_form,name='result_form'),
    path('no_marks',job.views.no_marks,name='no_marks'),
    path('verify_enroll',job.views.verify_enroll,name='verify_enroll')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
