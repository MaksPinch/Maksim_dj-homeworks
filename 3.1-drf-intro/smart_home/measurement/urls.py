from django.urls import path

from measurement.views import SensorListCreateView, SensorRetrieveUpdateView, MeasurementsCreateView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorListCreateView.as_view()),
    path('sensors/<pk>/', SensorRetrieveUpdateView.as_view()),
    path('measurements/', MeasurementsCreateView.as_view()),
]
