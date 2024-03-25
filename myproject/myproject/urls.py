
from django.contrib import admin
from django.urls import path
from yt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home', views.home,name="home"),
    path('select_stream',views.select_stream,name="select_stream"),
    path('watch',views.download_from_url),
    path('download/<int:id>/<str:quality>',views.download),

]
