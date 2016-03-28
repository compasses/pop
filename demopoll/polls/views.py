from django.template import Context, loader
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from polls.models import Choice
from polls.models import Poll


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('polls/index.html')
    c = Context({
        'latest_poll_list': latest_poll_list,
    })
    #return render(request, template_name, context)
    return HttpResponse(t.render(c))

def detail(request, poll_id):
    try:
        p = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll': p})

def results(request, poll_id):
    p = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/results.html', {'poll': p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, id=poll_id)
    try:
        selected_choice = p.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        # If the user chooses the wrong option, show error
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You have to choose the correct option.",
        })

    # Save the new number of votes
    selected_choice.votes += 1
    selected_choice.save()
    # Redirect a user to the detail view of the poll on which he or she just voted.
    return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))

# Create your views here.
