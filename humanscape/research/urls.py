from django.urls import path
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
# from research.views import ResearchViewSet
import research.views
from research.views import ResearchView


# router = routers.DefaultRouter()
# router.register('research', ResearchView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('list/', research.views.ResearchView.as_view(),),
    path('trials/<str:trial_id>', research.views.ResearchDetailView.as_view())
]
