from django.urls import path
from basepage.views import basepage, kursu_zapis

app_name='basepage'

urlpatterns = [
    path('', basepage),
    path('<int:elem_id>', kursu_zapis, name='form_zapis'),
]
