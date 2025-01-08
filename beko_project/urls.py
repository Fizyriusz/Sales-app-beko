from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produkty/', include('produkty.urls')),
    path('', lambda request: HttpResponseRedirect('/produkty/')),  # Przekierowanie do /produkty/, gdzie będzie widok home
]
