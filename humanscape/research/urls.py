from django.urls import path
from django.conf.urls import url
from django.contrib import admin
import research.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('list/', research.views.TrialListView.as_view(),),
    path('trials/<str:trial_id>', research.views.TrialDetailView.as_view())
]
