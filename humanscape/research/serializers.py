from rest_framework import serializers
from .models import Research

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = ('id', 'subject_number', 'subject_name', 'test_subject', 'study_period', 'department', 'research_institution',
                  'research_type', 'research_step', 'research_scope')