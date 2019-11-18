from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_board, name='board'),
    path('board', views.get_board_json, name='board_json'),
    path('player/<int:id>/', views.get_player_json, name='player'),
    path('player/create/', views.PlayerCreate.as_view(), name='player_create'),
    path('player/<int:pk>/update/', views.PlayerUpdate.as_view(),
        name='player_update'),
    path('players', views.get_players, name='players')
]
