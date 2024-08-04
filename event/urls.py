from django.urls import path
from . import views

urlpatterns = [
    path('',views.event_list,name='event_list'),
    path('<int:event_id>/',views.event_detail,name='event_detail'),
    path('create/',views.create_event,name='create_event'),
    path('<int:event_id>/join/',views.join_event,name='join_event'),
    path('myevents/',views.myevents,name='myevents'),
    path('<int:event_id>/addreview/',views.addreview ,name='addreview')
]