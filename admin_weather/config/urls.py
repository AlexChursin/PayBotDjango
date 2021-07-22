from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

#from bot_pay import views

urlpatterns = [
    path('', admin.site.urls),
  #  path('', views.api.urls)
]
urlpatterns += staticfiles_urlpatterns()