from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from urllib.request import urlopen
from .serializers import ResearchSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from .models import (
  Trial,
  Department,
  ResearchInstitution,
  ResearchType,
  ResearchStep,
  ResearchScope
)
import time
import urllib
import json
import ssl
from datetime import datetime, timedelta, date
import my_settings

def api_response():
    context     = ssl._create_unverified_context()
    url         = "https://api.odcloud.kr/api/3074271/v1/uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887?serviceKey="
    encode      = my_settings.API_KEY
    res         = urllib.request.urlopen(url + encode, context=context)
    json_str    = res.read().decode("utf-8")
    json_object = json.loads(json_str)

    return json_object['data']

def read_data():
    data = api_response()

    for datum in data[::-1]:
        research = Trial.objects.filter(trial_id=datum["과제번호"])
        if not research:
            if not datum["전체목표연구대상자수"]:
                datum["전체목표연구대상자수"] = 0
            department = Department.objects.filter(name=datum["진료과"]).first()
            if not department:
                department = Department.objects.create(name=datum["진료과"])
            research_institution = ResearchInstitution.objects.filter(name=datum["연구책임기관"]).first()
            if not research_institution:
                research_institution = ResearchInstitution.objects.create(name=datum["연구책임기관"])
            research_type = ResearchType.objects.filter(name=datum["연구종류"]).first()
            if not research_type:
                research_type = ResearchType.objects.create(name=datum["연구종류"])
            research_step = ResearchStep.objects.filter(name=datum["임상시험단계(연구모형)"]).first()
            if not research_step:
                research_step = ResearchStep.objects.create(name=datum["임상시험단계(연구모형)"])
            research_scope = ResearchScope.objects.filter(name=datum["연구범위"]).first()
            if not research_scope:
                research_scope = ResearchScope.objects.create(name=datum["연구범위"])

            Trial.objects.create(trial_id=datum["과제번호"], trial_name=datum["과제명"], department=department,
                                    research_institution=research_institution, research_type=research_type,
                                    research_step=research_step,
                                    research_scope=research_scope, study_period=datum["연구기간"],
                                    total_target_number=datum["전체목표연구대상자수"])
        # else:
        #     break

    return True


def api_job():
    print("task: " + str(time.time()))
    read_data()


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(api_job, 'cron', hour=0, id='api_get')


class ResearchView(GenericAPIView):
    read_data()
    startdate = date.today() - timedelta(days=7)
    startdate_time = datetime.combine(startdate, datetime.min.time())
    queryset = Trial.objects.filter(updated_at__gt=startdate_time)
    serializer = ResearchSerializer(queryset, many=True)
    serializer_class = ResearchSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ResearchDetailView(GenericAPIView):
    def get(self, request, trial_id):
        queryset = Trial.objects.filter(subject_number=trial_id).first()
        serializer = ResearchSerializer(queryset)
        return Response(serializer.data)

