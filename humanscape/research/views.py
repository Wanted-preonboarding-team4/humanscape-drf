from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import ResearchSerializer
from .models import Research, Department, ResearchInstitution, ResearchType, ResearchStep, ResearchScope
import csv

file_dir = '/Users/daminan/Desktop/humanscape-drf/'


def read_data(table_name):
    with open(file_dir + f'{table_name}.csv', 'r', encoding='CP949') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)[1:]
    # data = ApiResponse.api_response()
    for datum in data:
        if not datum[4]:
            datum[4] = 0
        department = Department.objects.filter(name=datum[2]).first()
        if not department:
            department = Department.objects.create(name=datum[2])
        research_institution = ResearchInstitution.objects.filter(name=datum[3]).first()
        if not research_institution:
            research_institution = ResearchInstitution.objects.create(name=datum[3])
        research_type = ResearchType.objects.filter(name=datum[6]).first()
        if not research_type:
            research_type = ResearchType.objects.create(name=datum[6])
        research_step = ResearchStep.objects.filter(name=datum[7]).first()
        if not research_step:
            research_step = ResearchStep.objects.create(name=datum[7])
        research_scope = ResearchScope.objects.filter(name=datum[8]).first()
        if not research_scope:
            research_scope = ResearchScope.objects.create(name=datum[8])
        research = Research.objects.filter(subject_number=datum[0])
        if not research:
            Research.objects.create(subject_number=datum[0], subject_name=datum[1], department=department,
                                    research_institution=research_institution, research_type=research_type,
                                    research_step=research_step,
                                    research_scope=research_scope, study_period=datum[5], test_subject=datum[4])
    return


class ResearchView(APIView):
    def get(self, request):
        read_data("research_data")
        return Response(status=200)
