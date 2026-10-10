from django.contrib import admin
from django.urls import path, include
from users.views import home, register_page, login_page , logout_page
from jobs.views import (
    jobs_page,
    job_detail_page,
    apply_page,
    my_applications_page,
    employer_dashboard,
    post_job,
    employer_my_jobs,
    employer_edit_job,
    employer_applicants,
    employer_update_application,
)


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
    path(
    'employer-dashboard/',
    employer_dashboard,
    name='employer-dashboard'
),
path(
    'post-job/',
    post_job,
    name='employer-post-job'
),
path('employer-my-jobs/', employer_my_jobs, name='employer-my-jobs'),
path(
    'employer-edit-job/<int:pk>/',
    employer_edit_job,
    name='employer-edit-job'
),
path(
    'employer-applicants/<int:pk>/',
    employer_applicants,
    name='employer-applicants'
),
path(
    'employer-update-application/<int:pk>/',
    employer_update_application,
    name='employer-update-application'
),

]