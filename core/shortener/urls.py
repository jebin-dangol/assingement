from django.urls import path
from .views import ShortURLViewSet

urlpatterns = [
    path('', ShortURLViewSet.as_view({'get': 'home', 'post': 'home'}), name='home'),
    path('dashboard/', ShortURLViewSet.as_view({'get': 'dashboard'}), name='dashboard'),
    path('<int:pk>/edit/', ShortURLViewSet.as_view({'get': 'edit_view', 'post': 'edit_view'}), name='edit_url'),
    path('<int:pk>/delete/', ShortURLViewSet.as_view({'get': 'delete_view', 'post': 'delete_view'}), name='delete_url'),
    path('<str:short_code>/', ShortURLViewSet.as_view({'get': 'redirect_view'}), name='redirect'),
]
