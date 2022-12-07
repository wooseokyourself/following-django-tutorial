from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F

from .models import Question, Choice
## /polls/
def index(request): 
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {
    'latest_question_list': latest_question_list,
  }
  # template = loader.get_template('polls/index.html')
  # return HttpResponse(template.render(context, request))
  return render(request, 'polls/index.html', context) #shorcut for above two lines

## /polls/1/
def detail(request, question_id):
  ## request: <WSGIRequest: GET '/polls/$(question_id)/'>
  # return HttpResponse("You're looking at question %s." % question_id)
  question = get_object_or_404(Question, pk=question_id) # object is "What's new?"
  return render(request, 'polls/detail.html', {'question': question})

## /polls/1/results/
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', {'question': question})

## /polls/1/vote/
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'polls/detail.html', {
      'question': question, 
      'error_message': "You didn't select a choice.",
    })
  else: 
    # selected_choice.votes += 1
    selected_choice.votes = F('votes') + 1 # Preventing race condition

    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice 
    # if a user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
