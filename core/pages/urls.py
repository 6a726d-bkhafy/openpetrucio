from django.urls import path
from .views import HostList,HostCreate,HostUpdate,UnwList,UnwDelete,SwitchList
from . import views

urlpatterns=[
    path('',HostList.as_view(),name='host_inventory'),
    path('add_host/',HostCreate.as_view(),name='add_host'),
    path('edit_host/<int:pk>/',HostUpdate.as_view(),name='edit_host'),
    path('delete_host/<int:id>/',views.delete_host,name='delete_host'),
    path('unknow/',UnwList.as_view(),name='unknow'),
    path('unknow/add_unw/<int:pk>',UnwDelete.as_view(),name='add_unw'),
    path('unw_to_main/<int:id>',views.unw_to_main,name='unw_to_main'),
    path('att/',views.att,name='att'),
    path('overview/<int:pk>',SwitchList.as_view(),name='overview'),
]