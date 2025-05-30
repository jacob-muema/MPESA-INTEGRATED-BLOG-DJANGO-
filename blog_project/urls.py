from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_register(request):
    return redirect('accounts:register')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_register, name='home_redirect'),  # Redirect to register first
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('dashboard/', include('admin_dashboard.urls')),  # Add admin dashboard URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
