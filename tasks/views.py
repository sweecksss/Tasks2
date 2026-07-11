from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Comment
from .mixins import UserIsOwnerMixin
from .forms import CommentForm, TaskForm

# Create your views here.
class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task-detail', pk=comment.task.pk)
            


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TaskUpdateView(UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

class TaskDeleteView(UserIsOwnerMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')

class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['content',]

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})