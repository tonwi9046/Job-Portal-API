from django.contrib import admin
from django.urls import path, include
from users.views import home, register_page, login_page , logout_page
from jobs.views import jobs_page, job_detail_page , apply_page , my_applications_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('jobs.urls')),
    path('', home, name='home'),
    path('register/', register_page, name='register-page'),
    path('login/', login_page, name='login-page'),
    path('jobs/', jobs_page, name='jobs-page'),
    path('jobs/<int:pk>/', job_detail_page, name='job-detail-page'),
    path('apply/<int:pk>/', apply_page, name='apply-page'),
    path('my-applications/', my_applications_page, name='my-applications-page'),
    path('logout/', logout_page, name='logout-page'),

]