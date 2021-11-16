from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Trial, Department, ResearchInstitution, ResearchType, ResearchStep, ResearchScope

from datetime import datetime, timedelta


class TrialListTestCase(APITestCase):
    def setUp(self):
        self.test_response ={"count": 1, "next": None, "previous": None, "results": [
            {"id": 1, "trial_id": "C131010", "trial_name": "test", "total_target_number": 200,
             "study_period": "3년", "department": 1, "research_institution": 1, "research_type": 1,
             "research_step": 1, "research_scope": 1}]}

        self.test_department = Department.objects.create(name="Hematology")
        self.test_research_institution = ResearchInstitution.objects.create(name="서울아산병원")
        self.test_research_type = ResearchType.objects.create(name="관찰연구")
        self.test_research_step = ResearchStep.objects.create(name="코호트")
        self.teat_research_scope = ResearchScope.objects.create(name="단일기관")

        self.test_trial1 = Trial.objects.create(trial_id="C131010", trial_name="test", total_target_number=200,
                                                study_period="3년",
                                                department=self.test_department,
                                                research_institution=self.test_research_institution,
                                                research_type=self.test_research_type,
                                                research_step=self.test_research_step
                                                , research_scope=self.teat_research_scope)

    def test_get_list_success(self):
        response = self.client.get(f'/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_list_pagination(self):
        for i in range(11):
            Trial.objects.create(trial_id=f"C131010{i}", trial_name="test", total_target_number=200,
                                                study_period="3년",
                                                department=self.test_department,
                                                research_institution=self.test_research_institution,
                                                research_type=self.test_research_type,
                                                research_step=self.test_research_step
                                                , research_scope=self.teat_research_scope)

        response = self.client.get(f'/list/')
        self.assertEqual(len(response.json()["results"]), 10)

    def test_get_list_time_limit(self):
        for i in range(11):
            Trial.objects.create(trial_id=f"C131010{i}", trial_name="test", total_target_number=200,
                                                study_period="3년",
                                                department=self.test_department,
                                                research_institution=self.test_research_institution,
                                                research_type=self.test_research_type,
                                                research_step=self.test_research_step,
                                                research_scope=self.teat_research_scope,
                                                updated_at=datetime.now()-timedelta(days=8)
                                 )

        response = self.client.get(f'/list/')
        response_json = response.json()["results"]
        update_date = response_json[0]["updated_at"][:10]
        self.assertEqual(len(response_json), 1)
        self.assertGreater(datetime.strptime(update_date, '%Y-%m-%d'), datetime.now()-timedelta(days=7))


