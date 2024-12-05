from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    ## url ajoutée au catégories 
    path('category_list/',views.category_list,name="categories"),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    ## url ajoutée au catégories 
    ## pour la gestion des favoris ##
    path('make-favorite/<int:post_id>/', views.function_make_favorite, name='make_favorite'),
    ## gestion des favoris ##

    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

]