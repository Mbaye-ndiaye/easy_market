from django.urls import path
from .views import register, login, type_depense, type_depense_detail, depense, depense_detail 
# from .views import TypeDepenseViewSet, DepenseViewSet


urlpatterns = [
        path('register/', register, name='register'),
        path('login/', login, name='login'),
        path('type-depenses/', type_depense, name='type-depense'),
        path('type-depense/<int:pk>', type_depense_detail, name='type-depense-detail'),
        path('depense/', depense, name='depense'),
        path('depense/<int:pk>', depense_detail, name='depense-detail'),

]