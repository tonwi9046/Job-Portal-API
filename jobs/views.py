from rest_framework import generics
from .models import Company, Category, Job, Application
from .serializers import CompanySerializer, CategorySerializer, JobSerializer, ApplicationSerializer
from django.shortcuts import render , redirect
from .models import Job


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
