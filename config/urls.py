
from django.contrib import admin
from django.urls import path, include

from users.views import (
    home,
    register_page,
    login_page,
    logout_page,
)

from jobs.views import (
    jobs_page,
    job_detail_page,
    apply_page,
    my_applications_page,
    employer_dashboard,
    post_job_page,
    employer_my_jobs,
    edit_job_page,
    delete_job_page,
    employer_applicants,
    update_application_status,
)


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # REST API
    path('api/users/', include('users.urls')),
    path('api/', include('jobs.urls')),

    # Job Seeker pages
    path('', home, name='home'),
    path('register/', register_page, name='register-page'),
    path('login/', login_page, name='login-page'),
    path('logout/', logout_page, name='logout-page'),

    path('jobs/', jobs_page, name='jobs-page'),
    path('jobs/<int:pk>/', job_detail_page, name='job-detail-page'),
    path('apply/<int:pk>/', apply_page, name='apply-page'),
    path(
        'my-applications/',
        my_applications_page,
        name='my-applications-page',
    ),

    # Employer pages
    path(
        'employer/',
        employer_dashboard,
        name='employer-dashboard',
    ),
    path(
        'employer/jobs/post/',
        post_job_page,
        name='employer-post-job',
    ),
    path(
        'employer/jobs/',
        employer_my_jobs,
        name='employer-my-jobs',
    ),
    path(
        'employer/jobs/<int:pk>/edit/',
        edit_job_page,
        name='employer-edit-job',
    ),
    path(
        'employer/jobs/<int:pk>/delete/',
        delete_job_page,
        name='employer-delete-job',
    ),
    path(
        'employer/jobs/<int:pk>/applicants/',
        employer_applicants,
        name='employer-applicants',
    ),
    path(
        'employer/applications/<int:pk>/<str:status>/',
        update_application_status,
        name='employer-update-application',
    ),
]
