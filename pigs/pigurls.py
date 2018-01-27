from django.conf.urls import url, include
from pigs import views

app_name = 'pigs'

urlpatterns = [
    
    url(r'^$',views.indexview.as_view(), name= 'index'),
    url(r'^pen(?P<pk>[0-9]+)/$', views.penview.as_view(), name = 'pen'),
    url(r'^pen(?P<pigpen>[0-9]+)/addration/$', views.addration, name= 'addration'),
    url(r'^pen(?P<pigpen>[0-9]+)/updateration(?P<rationid>[0-9]+)/$', views.updateration, name = 'updateration'),
    url(r'^pen(?P<pigpen>[0-9]+)/deletepigs/$', views.deleteallfrompen, name= 'dpig'),
    url(r'^pen(?P<pigpen>[0-9]+)/delete(?P<model>[a-zA-Z]+)/$', views.delete, name = 'delete'),
    url(r'^pen(?P<pigpen>[0-9]+)/deleteration(?P<id>[0-9]+)/$', views.deleteration, name='deleteration'),
    url(r'^pen(?P<pigpen>[0-9]+)/addpigs/$', views.changepigs, name= 'addpigs'),
    url(r'^pen(?P<pigpen>[0-9]+)/deadpigs/$', views.dead, name= 'deadpigs'),
    url(r'^pen(?P<pigpen>[0-9]+)/culledpigs/$', views.culled, name= 'culledpigs'),
    url(r'^pen(?P<pigpen>[0-9]+)/shippigs/$', views.shippigs, name= 'ship'),
    url(r'^pen(?P<pk>[0-9]+)/pigsforpen/$', views.pigsforpen.as_view(), name= 'pigsforpen'),
    url(r'^pen(?P<pk>[0-9]+)/deadculls/$', views.deadcull.as_view(), name = 'deadculls'),
    url(r'^Shipped/$', views.shippedpigs.as_view(), name= 'shippedpigs'),
    url(r'^pen(?P<pigpen>[0-9]+)/updatepigs(?P<pigid>[0-9]+)/$', views.updatepigs, name= 'updatepigs'),
    url(r'^pen(?P<pigpen>[0-9]+)/movepigs/$', views.movepigs, name= 'movepigs'),
    url(r'^Mixsheet/(?P<pigpen>[0-9]+)/$', views.mixsheet, name= 'mixsheet'),
    url(r'^additive(?P<pigpen>[0-9]+)/(?P<id>[0-9]+)/(?P<addn>.+)/$', views.additive, name='additive'),
    url(r'^chart/$', views.Chartview, name='chartjs'),
    url(r'^chartjs/$', views.chartdata, name='chart')
]