from django.urls import path
import club.views as views

urlpatterns = [
    path(
        "", views.ClubsView.as_view()
    ),  # should be searchable by a (name,category,rating,type) param
    # path('categories', views.ClubCategoriesView.as_view()),
    path("<int:id>", views.ClubView.as_view()),
    path("<int:id>/roadmap", views.RoadmapView.as_view()),
    path(
        "<int:id>/members", views.MembersView.as_view()
    ),  # should be searchable by a (name) param
    path("<int:id>/reviews", views.ReviewsView.as_view()),
    # path('<int:id>/document', views.ClubDocumentView.as_view()), todo
]
