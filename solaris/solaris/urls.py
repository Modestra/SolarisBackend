"""
URL configuration for solaris project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from solaris.view import *
from rest_framework import routers, permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter(trailing_slash=False)

schema_view = get_schema_view(
   openapi.Info(
      title="Solaris API",
      default_version='v1',
      description="API для ссылок проекта",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
#Регистрация готовых Views блоков для точек вхождения
router.register(r'forms', FeedbackFormApiView)
router.register(r'auth', AuthApiViewSet)
router.register(r'user', SchoolApiView)
router.register(r'rules', RulesApiViewSet)
router.register(r'shop', ShopApiViewSet)
router.register(r'competitions', CompetitionApiViewSet)
router.register(r'files', CompetitionFilesApiViewSet)
router.register(r'token', TokenApiView)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

]
