"""ASD_CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from cms_app.views import (MainPageView, OrdersToTakeView, CreateOrderView,
                           CloseRealizationView, CloseOrderListView,
                           CloseOrderDetailsView, CurrentInteruptionsView,
                           InterruptionsListView, CloseInterruptionView,
                           ChangeSaveView)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/login/'},
         name='logout'),
    path('', MainPageView.as_view(), name='index'),
    path('add_order', CreateOrderView.as_view(), name='add_order'),
    path('take_order', OrdersToTakeView.as_view(), name='orders_tt'),
    path('close_realization/<int:pk>', CloseRealizationView.as_view(),
         name='close'),
    path('close_order', CloseOrderListView.as_view(), name='close_order'),
    path('close_order/<int:pk>', CloseOrderDetailsView.as_view(),
         name='close_detail'),
    path('current_interruptions/', CurrentInteruptionsView.as_view(),
         name='current_inter'),
    path('interruptions', InterruptionsListView.as_view(),
         name='interruptions'),
    path('interruption/<int:pk>', CloseInterruptionView.as_view(),
         name='interruption'),
    path('change_save', ChangeSaveView.as_view(),
         name='change_save')
]

handler404 = 'cms_app.views.handler404'
handler500 = 'cms_app.views.handler500'
