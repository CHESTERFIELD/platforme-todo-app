from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from core.models import Todo
from core.forms import TodoForm, TodoFilterForm


class TodoListView(LoginRequiredMixin, ListView):
    login_url = '/'
    model = Todo
    template_name = 'todo_list.html'
    ordering = ['-created_at']
    # TODO: triage pagination issue
    # paginate_by = 2
    # paginate_orphans = 3

    def get_queryset(self):
        # filter tasks by user
        queryset = Todo.objects.filter(user=self.request.user)

        # if request contains priority param, make extra filtering
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # check whether task is overdue to render extra for the user
        context["now"] = timezone.now()
        # filter form with priority choices options
        context['filter_form'] = TodoFilterForm(self.request.GET)
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    login_url = '/'
    template_name = 'todo_form.html'
    form_class = TodoForm
    model = Todo

    def form_valid(self, form):
        # add user to the task
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # return to the user's list on success task creation
        return reverse_lazy('todo_list')


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/'
    template_name = 'todo_form.html'
    form_class = TodoForm
    model = Todo

    def get_success_url(self):
        # return to the user's list on success task creation
        return reverse_lazy('todo_list')


class TodoDetailView(LoginRequiredMixin, DetailView):
    login_url = '/'
    template_name = 'todo_detail.html'
    model = Todo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


@login_required
def index(request):
    return render(request, "base.html")


def update_create_todo_form_with_complete_before(request):
    priority = request.POST.get('priority')
    if priority == 'high':
        html = '''
            <label>Complete Before</label>
            <input type="datetime-local" class="input input-bordered w-full max-w-xs" id="complete_befor" name="complete_before">
            <div class="form-control">
            <label>Want be notified up to 3 hours</label>
            <input type="checkbox" name="to_be_notified" class="checkbox checkbox-success" id="id_to_be_notified">
            </div>
        '''
    else:
        html = ''  # Empty HTML if priority is not high
    return HttpResponse(html)


@login_required
@require_POST
def complete_todo(request, pk):
    """Marks task as completed and return partial object to be
    updated in UI.
    """
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.is_completed = True 
    todo.save()
    context = {'todo': todo}
    return render(request, 'todo_list_partial.html#todoitem-partial', context)


@login_required
@require_http_methods(['DELETE'])
def delete_todo(request, pk):
    """Deletes task.

    Return 'HTTPResponse' when deleted from table list
    """
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    if "redirect" in request.body.decode():
        response = HttpResponse(status=204)
        response["HX-Redirect"] = reverse('index')
    else:
        response = HttpResponse(status=204)
        response['HX-Trigger'] = 'delete-todo'
    return response
