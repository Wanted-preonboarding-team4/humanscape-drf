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


class TrialDetailTestCase(APITestCase):
    def setUp(self):

        self.test_department = Department.objects.create(name="Hematology")
        self.test_research_institution = ResearchInstitution.objects.create(name="서울아산병원")
        self.test_research_type = ResearchType.objects.create(name="관찰연구")
        self.test_research_step = ResearchStep.objects.create(name="코호트")
        self.teat_research_scope = ResearchScope.objects.create(name="단일기관")
        self.test_trial_id = "C131010"

        self.test_trial1 = Trial.objects.create(trial_id=self.test_trial_id, trial_name="test", total_target_number=200,
                                                study_period="3년",
                                                department=self.test_department,
                                                research_institution=self.test_research_institution,
                                                research_type=self.test_research_type,
                                                research_step=self.test_research_step
                                                , research_scope=self.teat_research_scope)

    def test_get_trial_detail_success(self):
        response = self.client.get(f'/trials/{self.test_trial_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_trial_detail_not_found(self):
        NOT_FOUND_TRIAL_ID = self.test_trial_id + "not_found"
        EXPECTED_RESPONSE = {'detail': 'C131010not_found 으로 찾을 수 없습니다.'}
        response = self.client.get(f'/trials/{NOT_FOUND_TRIAL_ID}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), EXPECTED_RESPONSE)

mock_response = {
    "page"        : 0,
    "perPage"     : 0,
    "totalCount"  : 0,
    "currentCount": 0,
    "data"        : [
        {
            "과제번호"        : "string",
            "과제명"         : "string",
            "진료과"         : "string",
            "연구책임기관"      : "string",
            "전체목표연구대상자수"  : "string",
            "연구기간"        : "string",
            "연구종류"        : "string",
            "임상시험단계(연구모형)": "string",
            "연구범위"        : "string"
        }
    ]
}
@patch("research.views.read_data", return_value=mock_response)
class ReadDataTestCase(APITestCase):
    def test_read_data(self, mock_get):
        response = mock_get.return_value
        self.assertEqual(response, mock_response)