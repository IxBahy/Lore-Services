from django.urls import  path
import club.views as views
urlpatterns=[
    # path('/', views.ClubsView.as_view()),#should be searchable by a (name,category,rating,type) param
    # path('/<int:pk>/', views.ClubView.as_view()),
    # path('/roadmap/', views.RoadmapView.as_view()),
    # path('/members/', views.ClubMembersView.as_view()),#should be searchable by a (name) param
    # path('/reviews', views.ClubReviewsView.as_view()),
    # path('/document', views.ClubDocumentView.as_view()),
    # path('/instructor', views.ClubInstructorView.as_view()),
]