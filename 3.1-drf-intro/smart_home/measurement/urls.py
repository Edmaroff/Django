from django.urls import path

from measurement.views import ReadCreateSensor, ReadUpdateSensor, CreateMeasurement

urlpatterns = [
    path('sensors/', ReadCreateSensor.as_view()),
    path('sensors/<int:pk>/', ReadUpdateSensor.as_view()),
    path('measurements/', CreateMeasurement.as_view()),

]
