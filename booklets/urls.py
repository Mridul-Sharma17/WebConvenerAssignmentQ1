from django.urls import path, include
from booklets import views

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_to_home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_home/', views.user_home, name='user_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('add_booklet/', views.add_booklet, name='add_booklet'),
    path('delete_booklet/<int:booklet_id>/', views.delete_booklet, name='delete_booklet'),
    path('accounts/', include('allauth.urls')),
]
