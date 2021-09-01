from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from bot_pay.views import router
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('', router, tags=['Referral'])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
#urlpatterns += staticfiles_urlpatterns()