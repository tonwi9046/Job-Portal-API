from rest_framework import generics
from .models import Company, Category, Job, Application
from .serializers import CompanySerializer, CategorySerializer, JobSerializer, ApplicationSerializer
from django.shortcuts import render , redirect
from .models import Job
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all().order_by('-applied_at')
    serializer_class = ApplicationSerializer


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

def jobs_page(request):
    jobs = Job.objects.all().order_by('-created_at')

    return render(request, 'jobs.html', {
        'jobs': jobs
    })
def jobs_page(request):
    jobs = Job.objects.all().order_by('-created_at')

    return render(request, 'jobs.html', {
        'jobs': jobs
    })
def job_detail_page(request, pk):

    job = Job.objects.get(id=pk)

    return render(request, 'job_detail.html', {
        'job': job
    })

def apply_page(request, pk):

    job = Job.objects.get(id=pk)

    if request.method == 'POST':

        resume = request.POST.get('resume')
        cover_letter = request.POST.get('cover_letter')

        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=resume,
            cover_letter=cover_letter
        )

        return redirect('/my-applications/')

    return render(request, 'apply.html', {
        'job': job
    })

def my_applications_page(request):

    applications = Application.objects.filter(
        applicant=request.user
    ).order_by('-applied_at')

    return render(request, 'my_applications.html', {
        'applications': applications
    })

@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(
        posted_by=request.user
    ).order_by('-created_at')

    return render(request, 'employer_dashboard.html', {
        'jobs': jobs,
    })


@login_required
def post_job_page(request):
    companies = Company.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        company = get_object_or_404(
            Company, pk=request.POST.get('company')
        )
        category = get_object_or_404(
            Category, pk=request.POST.get('category')
        )

        Job.objects.create(
            title=request.POST.get('title', '').strip(),
            company=company,
            category=category,
            location=request.POST.get('location', '').strip(),
            salary=request.POST.get('salary', '').strip(),
            job_type=request.POST.get('job_type'),
            description=request.POST.get('description', '').strip(),
            posted_by=request.user,
        )

        return redirect('employer-my-jobs')

    return render(request, 'post_job.html', {
        'companies': companies,
        'categories': categories,
    })


@login_required
def employer_my_jobs(request):
    jobs = Job.objects.filter(
        posted_by=request.user
    ).order_by('-created_at')

    return render(request, 'my_jobs.html', {
        'jobs': jobs,
    })


@login_required
def edit_job_page(request, pk):
    job = get_object_or_404(
        Job, pk=pk, posted_by=request.user
    )
    companies = Company.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        job.title = request.POST.get('title', '').strip()
        job.company = get_object_or_404(
            Company, pk=request.POST.get('company')
        )
        job.category = get_object_or_404(
            Category, pk=request.POST.get('category')
        )
        job.location = request.POST.get('location', '').strip()
        job.salary = request.POST.get('salary', '').strip()
        job.job_type = request.POST.get('job_type')
        job.description = request.POST.get('description', '').strip()
        job.save()

        return redirect('employer-my-jobs')

    return render(request, 'edit_job.html', {
        'job': job,
        'companies': companies,
        'categories': categories,
    })


@login_required
@require_POST
def delete_job_page(request, pk):
    job = get_object_or_404(
        Job, pk=pk, posted_by=request.user
    )
    job.delete()
    return redirect('employer-my-jobs')


@login_required
def employer_applicants(request, pk):
    job = get_object_or_404(
        Job, pk=pk, posted_by=request.user
    )
    applications = job.applications.select_related(
        'applicant'
    ).order_by('-applied_at')

    return render(request, 'applicants.html', {
        'job': job,
        'applications': applications,
    })


@login_required
@require_POST
def update_application_status(request, pk, status):
    application = get_object_or_404(
        Application,
        pk=pk,
        job__posted_by=request.user,
    )

    if status not in ('Accepted', 'Rejected'):
        return redirect(
            'employer-applicants',
            pk=application.job.pk,
        )

    application.status = status
    application.save(update_fields=['status'])

    return redirect(
        'employer-applicants',
        pk=application.job.pk,
    )
