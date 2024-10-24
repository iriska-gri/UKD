from django.urls import path
from . import views

urlpatterns = [
    path('load/', views.FileUploadView.as_view()),
    path('<str:statistictype>/reporting/docs/', views.DocksData.as_view()),
    path('fb1/reporting/list/', views.ListDataFBoneView.as_view()),
    path('fb1/reporting/monitoring/', views.MonitoringDataFBoneView.as_view()),
    path('fb1/reporting/monitoring/modal/', views.MonitoringDataFBoneView.as_view()),
    path('fb1/reporting/monitoringifns/', views.MonitoringDataFBoneView.as_view()),
    path('fb1/reporting/monitoringifns/modal/', views.MonitoringDataFBoneView.as_view()),
    path('fb1/reporting/justify/', views.JustifyDataFBoneView.as_view()),
    path('fb1/reporting/justify/create/', views.CreateJustifyFBone.as_view()),
    path('dynamics/list/', views.GetDynamics.as_view()),
    path('getfilters/', views.GetFilters.as_view()),
    path('passport/', views.PassportView.as_view()),
    path('passport/<int:pk>/', views.PassportDetailView.as_view()),
    # path('helper/', views.Helper.as_view()),

]