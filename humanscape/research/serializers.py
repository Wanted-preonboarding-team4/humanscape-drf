from rest_framework import serializers
from .models import Trial

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trial
        fields = ('id', 'trial_id', 'trial_name', 'total_target_number', 'study_period', 'department', 'research_institution',
                  'research_type', 'research_step', 'research_scope', 'created_at', 'updated_at')