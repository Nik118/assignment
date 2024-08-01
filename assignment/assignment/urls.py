"""
URL configuration for assignment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from metadata.views import CategoryView, DepartmentView, SubCategoryView, SKUView
from metadata.views import LocationViewSet

router = DefaultRouter()
router.register(r'location', LocationViewSet, basename="locations")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/location/<int:location_id>/department', DepartmentView.as_view()),
    path('api/v1/location/<int:location_id>/department/<int:department_id>', DepartmentView.as_view()),
    path('api/v1/location/<int:location_id>/department/<int:department_id>/category', CategoryView.as_view()),
    path('api/v1/location/<int:location_id>/department/<int:department_id>/category/<int:category_id>', CategoryView.as_view()),
    path('api/v1/location/<int:location_id>/department/<int:department_id>/category/<int:category_id>/subcategory', SubCategoryView.as_view()),
    path('api/v1/location/<int:location_id>/department/<int:department_id>/category/<int:category_id>/subcategory/<int:subcategory_id>', SubCategoryView.as_view()),
    path('api/v1/skus/', SKUView.as_view()),
]