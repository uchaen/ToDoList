from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form): 
        user = form.save()
        if user is not None:  # 회원가입 완료 시 자동 로그인
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
    

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) #다른사람꺼 못보게
        context['count'] = context['tasks'].filter(complete=False).count() #complete되지않은 task개수 count해줌
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input) #검색 설정. icontains(~포함)대신 startswith(~로 시작하는) 가능
        context['search_input'] = search_input        

        return context



class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form): #user specific data를 위해. 할일 생성 시 user 선택지가 기본이 본인임
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description'] # '__all__'로 하면 전부 보임
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields = '__all__' 
    success_url = reverse_lazy('tasks')


# 할일 complete하거나 취소할수있는 함수
def crossOff(request,*args, pk):
    item = Task.objects.get(pk=pk)
    item.complete=True
    item.save()
    return redirect('tasks')

def uncross(request,*args, pk):
    item = Task.objects.get(pk=pk)
    item.complete=False
    item.save()
    return redirect('tasks')