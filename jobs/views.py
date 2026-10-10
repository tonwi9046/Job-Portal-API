
from rest_framework import generics
from .models import Company, Category, Job, Application
from .serializers import (
    CompanySerializer,
    CategorySerializer,
    JobSerializer,
    ApplicationSerializer,
)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated


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
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.all()

    def update(self, request, *args, **kwargs):
        job = self.get_object()

        if not (request.user.is_staff or job.posted_by == request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can only edit your own jobs."
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        job = self.get_object()

        if not (request.user.is_staff or job.posted_by == request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can only delete your own jobs."
            )

        return super().destroy(request, *args, **kwargs)


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Application.objects.all().order_by('-applied_at')

        return Application.objects.filter(
            applicant=user
        ).order_by('-applied_at')

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)



class ApplicationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Application.objects.all()

        return Application.objects.filter(applicant=user)


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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def my_applications_page(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).order_by('-applied_at')

    return render(request, 'my_applications.html', {
        'applications': applications
    })


@login_required(login_url='/login/')
def employer_dashboard(request):
    jobs = Job.objects.filter(
        posted_by=request.user
    ).order_by('-created_at')

    return render(request, 'employer_dashboard.html', {
        'jobs': jobs
    })


@login_required(login_url='/login/')
def employer_my_jobs(request):
    jobs = Job.objects.filter(
        posted_by=request.user
    ).order_by('-created_at')

    return render(request, 'employer_my_jobs.html', {
        'jobs': jobs
    })


@login_required(login_url='/login/')
def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company_id = request.POST.get('company')
        category_id = request.POST.get('category')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        job_type = request.POST.get('job_type')
        description = request.POST.get('description')

        Job.objects.create(
            title=title,
            company_id=company_id,
            category_id=category_id,
            location=location,
            salary=salary,
            job_type=job_type,
            description=description,
            posted_by=request.user
        )

        return redirect('/employer-dashboard/')

    companies = Company.objects.all()
    categories = Category.objects.all()

    return render(request, 'post_job.html', {
        'companies': companies,
        'categories': categories
    })


@login_required(login_url='/login/')
def employer_edit_job(request, pk):
    job = Job.objects.get(pk=pk, posted_by=request.user)

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company_id = request.POST.get('company')
        job.category_id = request.POST.get('category')
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary')
        job.job_type = request.POST.get('job_type')
        job.description = request.POST.get('description')
        job.save()

        return redirect('/employer-my-jobs/')

    return render(request, 'post_job.html', {
        'job': job,
        'companies': Company.objects.all(),
        'categories': Category.objects.all(),
        'edit_mode': True,
    })


@login_required(login_url='/login/')
def employer_applicants(request, pk):
    job = Job.objects.get(pk=pk, posted_by=request.user)

    applications = Application.objects.filter(
        job=job
    ).select_related('applicant')

    return render(request, 'employer_applicants.html', {
        'job': job,
        'applications': applications,
    })

@login_required(login_url='/login/')
def employer_update_application(request, pk):
    if request.method == 'POST':
        application = Application.objects.get(
            pk=pk,
            job__posted_by=request.user
        )

        status = request.POST.get('status')

        if status in ['Accepted', 'Rejected']:
            application.status = status
            application.save()

        return redirect(
            f'/employer-applicants/{application.job.pk}/'
        )

    return redirect('/employer-dashboard/')

