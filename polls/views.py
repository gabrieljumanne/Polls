from typing import Any
from django.db.models import F, Count
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render 
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice




# Create your views here.

"""_summary_
    Render object returns the Https Response object
"""

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """Return five top questions"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()).annotate(
                choice_count = Count("choice")
            ).filter(
                choice_count__gt=0
            ).order_by(
                "-pub_date"
            )[:5]

class DetailView(generic.DetailView):
    template_name = "polls/detail.html"
    #model = Question
    
    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(
            pub_date__lte=timezone.now()).annotate(
                choice_count = Count("choice")
            ).filter(
                choice_count__gt = 0
            ).order_by(
                "-pub_date"
            )



def vote(request, question_id):
    question= get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])        
        
    except (KeyError, Choice.DoesNotExist):
        
        return render(
            request, "polls/index.html",
            {
                "question": question,
                "error_message":"You did not select the choice.",
            },
        )
    else:
        
        selected_choice.votes = F("votes") + 1 
        selected_choice.save()
        
        #redirect using reverse().
        return HttpResponseRedirect(reverse("polls:result", args=(question.id,)))


class ResultView(generic.DetailView):
    template_name = "polls/result.html"
    
    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).annotate(
            choice_count = Count("choice")
        ).filter(
            choice_count__gt = 0
        )
