from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('by/<username>/', views.UserTwitt.as_view(), name = 'for_user'),
    path('by/<username>/<int:pk>', views.SingleTwitt.as_view(), name = "singletwitt"),
    path('new/', views.CreateTwitt.as_view(), name = 'createtwitt'),
    path('update/<int:pk>', views.UpdateTwitt.as_view(), name = 'updatetwitt'),
    path('delete/<int:pk>', views.DeleteTwitt.as_view(), name = 'deletetwitt'),
    path('profile/', views.edit_photo, name = 'profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
