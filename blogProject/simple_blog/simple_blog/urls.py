import django.contrib.auth.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # Include the blog app URLs
    path('users/', include('users.urls')),  # Include the users app URLs
    # path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
    # path('<path:resource>', RedirectView.as_view(url='/blog/')),  # Redirect all undefined paths to /blog/,
    # path('', RedirectView.as_view(url='/blog/')),  # Redirect all undefined paths to /blog/
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)