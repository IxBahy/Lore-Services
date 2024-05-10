from django.urls import  path
import student.views as views
urlpatterns=[
  path('clubs', views.StudentClubsView.as_view()),
  path('join-club', views.StudentClubActionsView.as_view()),
  path('progress', views.StudentProgressView.as_view()),
  path('complete-week', views.StudentCompletedWeekView.as_view()),
  path('friends', views.StudentFriendsView.as_view()),
]