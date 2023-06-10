from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from matplotlib.pyplot import cla, title
from requests import request
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
class Customloginview(LoginView):
    template_name='todo/login.html'
    fields='__all__'
    redirect_authenticated_user=True
    

    def get_success_url(self):
        return reverse_lazy('tasks')

class Tasklist(LoginRequiredMixin,ListView):
    login_url='login' #or set is from settings.py as done
    model=Task
    context_object_name= 'tasks'
    template_name='todo/task_list.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        searchinp=self.request.GET.get('searchinp') or ''
        if searchinp:
            context['tasks']=context['tasks'].filter(title__icontains=searchinp)
        context['searchinp']=searchinp
        # print(context)
        return context
        

class Taskdetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
    template_name='todo/task.html'

class Taskcreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks') #redirect
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(Taskcreate,self).form_valid(form)

class Taskupdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

class Taskdelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')

class Register(FormView):
    template_name='todo/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(Register,self).form_valid(form)
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register,self).get(*args,**kwargs)