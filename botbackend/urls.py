from django.urls import path
from . import views

urlpatterns = [
    path('pack/list/', views.packlist, name='pack_list'),
    path('path/create/', views.PackCreateView.as_view(), name='pack_create'),
    path('path/<int:pk>/edit/', views.PackUpdateView.as_view(), name='pack_edit'),
    path('path/<int:pk>/delete/', views.PackDeleteView.as_view() , name='pack_del'),
    path('card/list/', views.cardlist, name='card_list_all'),
    path('card/create/', views.CardCreateView.as_view(), name='card_create'),
    path('card/<int:pk>/edit/', views.CardUpdateView.as_view(), name='card_edit' ),
    path('card/<int:pk>/delete/', views.CardDeleteView.as_view() , name='card_del'),
    path('steps/list/', views.stepslist, name='steps_list'),
    path('steps/create/', views.StepsCreateView.as_view() , name='steps_create'),
    path('steps/<int:pk>/edit/', views.StepsUpdateView.as_view(), name='steps_edit' ),
    path('steps/<int:pk>/delete/', views.StepsDeleteView.as_view() , name='steps_del'),
    path('chatusers/list/', views.chatuserlist, name='chatuser_list'),
    path('chatuser/<int:pk>/activate/', views.chatuseractivate, name='chatuser_activate'),
    path('chatuser/<int:pk>/deactivate/', views.chatuserdeactivate, name='chatuser_deactivate'),
]