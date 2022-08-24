from django.shortcuts import  redirect,render,get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import Homework,Todo
from django.views import generic
from . forms import Note,NotesForm,HomeworkForm, TodoForm, DashboardForm,UserRegisterationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.views import generic
import requests
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

@login_required
def home(request):
    return render(request, 'dashboard/home.html' )

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Note(user=request.user, title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")
    else:
        form = NotesForm()
    form = NotesForm()
    notes = Note.objects.filter(user=request.user)
    context = {'notes':notes, 'form':form}
    return render(request, 'dashboard/notes.html', context)

def delete_note(request,pk=None):
    Note.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    print("INSID GENERIC VIEW")
    model = Note 

def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished'] 
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f"Homework Added from {request.user.username} !!")
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else :
        homework_done = False
    context = {
        'homeworks':homeworks,
        'homework_done':homework_done, 
        'form':form}
    return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished'] 
                if finished == 'on':
                    finished = True
                else:
                    finished = False

            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(str(todo)) == 0:
        todos_done = True
    else :
        todos_done = False
    context = {
        'todos' : todo,
        'todos_done' : todos_done,
        'form' : form
    }
    return render(request, 'dashboard/todo.html', context)



def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        response = requests.get(url)
        
        answer = response.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'] [i]['volumeInfo']['title'],
                'subtitle':answer['items'] [i]['volumeInfo'].get('subtitle'),
                'description':answer['items'] [i]['volumeInfo'].get('description'),
                'count':answer['items'] [i]['volumeInfo'].get('pageCount'),
                'catagories':answer['items'] [i]['volumeInfo'].get('catagories'),
                'rating':answer['items'] [i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'] [i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'] [i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict) 
            context = {
                'form':form,
                'results' : result_list
            }
        return render(request, 'dashboard/books.html',context )
    else:
        form = DashboardForm()
    context = {'form' : form}
    return render(request, 'dashboard/books.html',context )

def register(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!!")
            return redirect('login')
    else: 
        form = UserRegisterationForm()
    context = {'form' : form}
    return render(request, 'dashboard/register.html',context )

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done = True
    else:
        homework_done = False

    if len(todos)==0:
        todos_done = True
    else:
        todos_done = False
        
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'homeworks' : homeworks,
        'todos' : todos,
        'homework_done' : homework_done,
        'todos_done' : todos_done,
        'u_form': u_form,
        'p_form': p_form
    
    }
    return render(request, 'dashboard/profile.html',context)


#BLOG PART


def blog(request):
    context={
        'posts' : Post.objects.all()
    }
    return render(request, 'dashboard/blogs.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'dashboard/home.html'  # <app>/<model>_<viewtype>.html
    cotext_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UserPostListView(ListView):
    model = Post
    template_name = 'dashboard/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False