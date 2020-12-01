from django.conf.urls import url
from pgi_app import views

app_name= 'pgi_app'
urlpatterns=[
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^student_profile/$',views.student_profile,name='student_profile'),
    url(r'^check_status/$',views.check_status,name='check_status'),
    url(r'^make_request/$',views.make_request,name='make_request'),
    url(r'^available_rooms/$',views.available_rooms,name='available_rooms'),
    url(r'^oi_profile/$',views.oi_profile,name='oi_profile'),
    url(r'^oi_request/$',views.oi_request,name='oi_request'),
    url(r'^si_profile/$',views.si_profile,name='si_profile'),
    url(r'^si_request/$',views.si_request,name='si_request'),
    url(r'^guard_request/$',views.guard_request,name='guard_request'),
    url(r'^guard_profile/$',views.guard_profile,name='guard_profile'),
]
