from django.db import models

class Research(models.Model):
    subject_number       = models.CharField(max_length=10)
    subject_name         = models.CharField(max_length=200)
    test_subject         = models.IntegerField
    study_period         = models.CharField(max_length=10)
    department           = models.ForeignKey('Department', on_delete=models.CASCADE)
    research_institution = models.ForeignKey('ResearchInstitution', on_delete=models.CASCADE)
    research_type        = models.ForeignKey('ResearchType', on_delete=models.CASCADE)
    research_model       = models.ForeignKey('ResearchModel', on_delete=models.CASCADE)
    research_scope       = models.ForeignKey('ResearchScope', on_delete=models.CASCADE)

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


class ResearchModel(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'research_model'


class ResearchScope(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'research_scope'