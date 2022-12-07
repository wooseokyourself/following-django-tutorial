from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
  # views' methods should get request parameter as http request.
  # other parameter defines like <int:question_id>, with specific name.

  # ex: /polls/index/
  path('index/', views.index, name='index'),

  #ex: /polls/$(question_id)/
  path('<int:question_id>/', views.detail, name='detail'),

  #ex: /polls/$(question_id)/results/
  path('<int:question_id>/results/', views.results, name='results'),

  #ex: /polls/$(question_id)/vote/
  path('<int:question_id>/vote/', views.vote, name='vote')
]
