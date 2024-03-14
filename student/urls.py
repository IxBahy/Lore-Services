from django.urls import  path
import student.views as views
urlpatterns=[
  path('<int:id>', views.StudentsView.as_view()),
  # path('<int:id>/clubs', views.StudentClubsView.as_view()),
  # path('<int:id>/progress', views.StudentProgressView.as_view()),
  # path('<int:id>/completed', views.StudentCompletedView.as_view()),
  # path('<int:id>/friends', views.StudentFriendsView.as_view()),
]