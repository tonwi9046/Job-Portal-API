from rest_framework import serializers
from .models import Company, Category, Job, Application


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'location']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company',
            'category',
            'location',
            'salary',
            'job_type',
            'description',
            'posted_by',
            'created_at'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'applicant',
            'resume',
            'cover_letter',
            'status',
            'applied_at'
        ]
        read_only_fields = ['status', 'applied_at']