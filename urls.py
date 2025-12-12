from django.urls import path
from . import views

urlpatterns = [
    path('auth/register', views.register, name='register'),
    path('auth/login', views.login, name='login'),
    path('sweets', views.SweetListCreateView.as_view(), name='sweet-list-create'),
    path('sweets/search', views.SweetSearchView.as_view(), name='sweet-search'),
    path('sweets/<int:pk>', views.SweetDetailView.as_view(), name='sweet-detail'),
    path('sweets/<int:pk>/purchase', views.purchase_sweet, name='sweet-purchase'),
    path('sweets/<int:pk>/restock', views.restock_sweet, name='sweet-restock'),
]
