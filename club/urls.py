from django.urls import  path
import club.views as views
urlpatterns=[
    path('', views.ClubsView.as_view()),#should be searchable by a (name,category,rating,type) param
    path('<int:pk>', views.ClubView.as_view()),
    path('<int:pk>/roadmap', views.RoadmapView.as_view()),
    path('<int:pk>/members', views.MembersView.as_view()),#should be searchable by a (name) param
    path('<int:pk>/reviews', views.ReviewsView.as_view()),
    # path('<int:pk>/document', views.ClubDocumentView.as_view()),
    # path('<int:pk>/instructor', views.ClubInstructorView.as_view()),
]