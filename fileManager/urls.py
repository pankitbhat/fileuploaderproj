from django.urls import path
from django.conf.urls import include
from .views import UserFileUpload, UserFileOperations, UserFileCopy, FileSearchView

from rest_framework import routers

router = routers.DefaultRouter()
router.register("filename/search", FileSearchView, basename="filename-search")

urlpatterns = [
    path('upload/', UserFileUpload.as_view(), name='file-upload'),
    path('fileops/', UserFileOperations.as_view()),
    path('copy/', UserFileCopy.as_view()),
    path('', include(router.urls))
]
