from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo
# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task_name')
        new_todo = Todo(user = request.user , todo_name = task)
        new_todo.save()
    all_todos = Todo.objects.filter(user = request.user)
    context = {
            'todos' : all_todos
        }
    return render(request , 'todoapp/index.html' , context)

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 8:
            messages.error(request , 'Password Must be atleast 8 charactor')
            return render(request, 'todoapp/register.html')
        
        get_user_by_username = User.objects.filter(username=username)
        if get_user_by_username:
            messages.error(request , 'Username already exist , try another one')
            return render(request, 'todoapp/register.html')
        get_user_by_email = User.objects.filter(email=email)
        if get_user_by_email:
            messages.error(request , 'User with this Email already exist , try another one')
            return render(request, 'todoapp/register.html')
        
        new_user = User.objects.create_user(first_name=firstname , last_name=lastname , email=email , username=username , password=password1)
        new_user.save()
        messages.success(request , 'User Registerd Successfully now Login')
        return render(request, 'todoapp/login.html')
    return render(request , 'todoapp/register.html' , {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(request , username=username , password=password)
        if validate_user is not None:
            login(request , validate_user)
            return redirect('homepage' )
        else:
            messages.error(request , 'User details are wrong or Does not exist')
            return render(request, 'todoapp/login.html')
    return render(request, 'todoapp/login.html' , {})

def delete_task(request , name):
    get_todo = Todo.objects.get(user = request.user , todo_name = name)
    get_todo.delete()
    return redirect('homepage')

def update_task(request , name):
    get_todo = Todo.objects.get(user = request.user , todo_name = name)
    get_todo.status = True
    get_todo.save()
    return redirect('homepage')


