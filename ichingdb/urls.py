from django.urls import path

from . import views

app_name = 'ichingdb'
urlpatterns = [
    # ex: /ichingdb
    path('', views.index, name='index'),
    # ex: /ichingdb/cast
    path('cast/', views.ConsultationCreate.as_view(), name='cast'),
    # ex: /ichingdb/random
    path('random/', views.ConsultationCreateRandom.as_view(), name='random'),
    # ex: /ichingdb/5/
    path('<int:cid>/', views.reading, name='reading'),
    # ex: /ichingdb/5/update/
    path('<int:pk>/update/', views.ConsultationUpdate.as_view(), name='update'),
    # ex: /ichingdb/5/delete/
    path('<int:pk>/delete/', views.ConsultationDelete.as_view(), name='delete'),
]
