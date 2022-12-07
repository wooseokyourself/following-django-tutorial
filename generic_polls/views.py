from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone
from .models import Question, Choice

def get_published_question_queryset():
    question_queryset = Question.objects.filter(pub_date__lte=timezone.now())
    for q in question_queryset.iterator():
        if Choice.objects.filter(question=q.pk).count() == 0:
            question_queryset = question_queryset.exclude(pk=q.pk)
    return question_queryset

class IndexView(generic.ListView): 
    template_name = 'generic_polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return get_published_question_queryset().order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'generic_polls/detail.html'

    def get_queryset(self): 
        return get_published_question_queryset()

class ResultsView(generic.DetailView): 
    model = Question
    template_name = 'generic_polls/results.html'

    def get_queryset(self):
        return get_published_question_queryset()


def vote(request, question_id):
    question = get_object_or_404(get_published_question_queryset(), pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'generic_polls/detail.html', {
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
        return HttpResponseRedirect(reverse('generic_polls:results', args=(question.id,)))
