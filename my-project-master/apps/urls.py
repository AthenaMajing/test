from django.conf.urls import url

from apps import views

urlpatterns = [
    url(r'^login/$',views.LoginView.as_view()),
    url(r'^homes/$',views.UserView.as_view()),
    url(r'addpermission/$',views.PermissionView.as_view()),
    url(r'showuser/(?P<select_name>\w+)/(?P<page>\d+)/$',views.UserInfoShow.as_view()),
    url(r'^addnewpermission/$',views.CreatPermissionView.as_view()),
    url(r'showpermission/(?P<select_name>\w+)/(?P<page>\d+)/$', views.PermissionInfoShow.as_view()),
    url(r'^addnewrole/$', views.CreatRoleView.as_view()),
    url(r'showrole/(?P<select_name>\w+)/(?P<page>\d+)/$', views.RoleInfoShow.as_view()),
    url(r'^users/(?P<user_id>\d+)/(?P<page>\d+)/$',views.UpdateInfoViewSet.as_view({'get': 'retrieve'})),
    url(r'^users/(?P<pk>\d+)/$',views.UpdateInfoViewSet.as_view({'post': 'updates'})),
    url(r'^permission/(?P<permission_id>\d+)/(?P<page>\d+)/$',views.UpdatePermissionViewSet.as_view({'get': 'retrievepermission'})),
    url(r'^permission/(?P<pk>\d+)/$',views.UpdatePermissionViewSet.as_view({'post': 'updatespermission'})),
    # url(r'^(?P<pk>[0-9]+)/$', views.snippet_detail)
]