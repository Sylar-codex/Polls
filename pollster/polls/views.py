from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Question, Choice

#get question and display them
def index(request) :
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', context)

#show specific questions and choices
def details(request, question_id) :
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist :
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question':question})

#get questions and display result
def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html',{'question':question})

#vote for a question choice
def vote(request, question_id) :
    print(request.method)
    #print(request.POST['choice'])
    question = get_object_or_404(Question, pk= question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist) :
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message':"You didn't select a choice.",
        })
    else :
        selected_choice.votes +=1
        selected_choice.save()

        # Always return an HttpResponseRedirect after succesfully dealing
        # with POST data. This prevents data from being posted twice if a user 
        # hits the back button
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))