from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


class ReadCreateSensor(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class ReadUpdateSensor(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

class CreateMeasurement(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
