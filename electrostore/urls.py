from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('user/login/', views.uslogin, name='uslogin'),
    path('logout/', views.uslogout, name='uslogout'),
    path('accounts/profile/', views.authemail, name='authemail'),  # CUSTOM
    path('myapp/', include('myapp.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('paypal/', include('paypal.standard.ipn.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
