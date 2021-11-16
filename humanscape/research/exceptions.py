from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = 404
    def __init__(self, field_name):
        self.default_detail = f"{field_name} 으로 찾을 수 없습니다."
        super(NotFoundException, self).__init__()
