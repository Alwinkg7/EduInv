from django.contrib import admin
from django.urls import path, include
import EduInvApp.urls, AdminApp.urls
from EduInv import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('AdminApp/', include(AdminApp.urls)),
    path('EduInvApp/', include(EduInvApp.urls)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
