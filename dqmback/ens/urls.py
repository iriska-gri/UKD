from django.urls import path
from . import views

urlpatterns = [
    # path('load/', views.FileUploadView.as_view()),
    # path('<str:statistictype>/reporting/docs/', views.DocksData.as_view()),
    path('reporting/list/', views.ListDataFBoneView.as_view()),
    path('reporting/monitoring/', views.MonitoringDataFBoneView.as_view()),
    path('reporting/monitoring/modal/', views.MonitoringDataFBoneView.as_view()),
    path('reporting/monitoringifns/', views.MonitoringDataFBoneView.as_view()),
    path('reporting/monitoringifns/modal/', views.MonitoringDataFBoneView.as_view()),
    # path('ens/reporting/justify/', views.JustifyDataFBoneView.as_view()),
    # path('ens/reporting/justify/create/', views.CreateJustifyFBone.as_view()),
    # path('dynamics/list/', views.GetDynamics.as_view()),
    # path('getfilters/', views.GetFilters.as_view()),
    path('passport/', views.PassportView.as_view()),
    # path('passport/<int:pk>/', views.PassportDetailView.as_view()),
    path('dashboard/', views.Dashboard.as_view()),
  

]