from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class Research(models.Model):
    subject_number       = models.CharField(max_length=10)
    subject_name         = models.CharField(max_length=200)
    test_subject         = models.PositiveIntegerField(default=0, blank=True)
    study_period         = models.CharField(max_length=10, blank=True, default='')
    department           = models.ForeignKey('Department', on_delete=models.CASCADE)
    research_institution = models.ForeignKey('ResearchInstitution', on_delete=models.CASCADE)
    research_type        = models.ForeignKey('ResearchType', on_delete=models.CASCADE)
    research_step        = models.ForeignKey('ResearchStep', on_delete=models.CASCADE)
    research_scope       = models.ForeignKey('ResearchScope', on_delete=models.CASCADE)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(default=now)

    class Meta:
        db_table = 'research'


class Department(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'department'


class ResearchInstitution(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'research_institution'


class ResearchType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'research_type'


class ResearchStep(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'research_step'


class ResearchScope(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'research_scope'