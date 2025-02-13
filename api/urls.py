from django.urls import path
from .views import  type_depense_detail,  type_depense_list, depense_list, depense_detail 
# from .views import TypeDepenseViewSet, DepenseViewSet


urlpatterns = [
        path('type-depenses/', type_depense_list, name='type-type_depense_list'),
        path('type-depenses/<int:pk>', type_depense_detail, name='type-depense-detail'),
        path('depenses/', depense_list, name='depense_list'),
        path('depenses/<int:pk>/', depense_detail, name='depense_detail'),

]