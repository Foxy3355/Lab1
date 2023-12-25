from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, DeleteView, RedirectView
from .models import Question, Choice, User, VotedUsers
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import RegistrationForm, MyAuthenticationForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView


def homeView(request):
    return render(request, 'home.html')


def regView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password'])
                new_user.password2 = 'NULL'
                new_user = form.save()
                login(request, new_user)
                # return render(request, 'polls/reg_success.html')
                return redirect('polls:login')
        else:
            return render(request, 'polls/registration.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'polls/registration.html', {'form': form})


class MyLoginView(LoginView):
    template_name = 'polls/login.html'
    form = MyAuthenticationForm
    next_page = 'polls:index'

    # def get_success_url(self):
    #     return reverse_lazy('polls:index')


class Profile(UpdateView):
    model = User
    fields = ['name', 'surname', 'mail', 'avatar']
    success_url = reverse_lazy('polls:index')
    template_name = 'polls/accounts/profile.html'


def delete_profile(request, pk):
    obj = User.objects.get(pk=pk)
    obj.delete()
    return render(request, 'polls/delete_success.html')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def dispatch(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if VotedUsers.objects.filter(user=request.user, question=question.pk).exists():
            var = int(kwargs['pk'])
            # return RedirectView.as_view(url='polls:results')(request, *args, **kwargs) 3
            return redirect(reverse('polls:results', args=(var,)))

        stub = Question.objects.get(pk=kwargs['pk'])
        if stub.was_published_recently():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('polls:index'))


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = Question.objects.get(pk=self.kwargs['pk'])
        # total_votes = q.choice_set.aggregate(total_votes=Sum('votes'))['total_votes']
        total_votes = q.choice_set.aggregate(total_votes=Sum(Cast('votes', FloatField())))['total_votes']
        choices_with_percent = (q.choice_set.annotate(percent=(F('votes') / total_votes) * 100)
                                .values('choice_text', 'percent'))
        context['question'] = q
        context['total_votes'] = total_votes
        context['choices_with_percents'] = choices_with_percent
        return context


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        if VotedUsers.objects.filter(user=request.user, question=question.pk).exists():
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else:
            VotedUsers.objects.create(user=request.user, question=question)
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class HistoryList(generic.ListView):
    model = Question
    template_name = 'polls/historylist.html'
    context_object_name = 'lst'


class BBLogoutView(LoginRequiredMixin, LogoutView):
   template_name = 'polls/logout.html'