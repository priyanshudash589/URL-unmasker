from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.home,name="home"),
   path('extreq/',views.chrome_req, name="chromereq"),
   path('shortsafeurl/',views.create_safe_short_urls,name="safeshorturls"),
   path('api/v1/unsafeurls/', views.unsafeurls.as_view(),name='api-unsafeurls-view'),
	path('api/v1/unsafeurls/<int:pk>/', views.unsafeurls_details.as_view(),name='api-unsafeurls-details-view'),

]
