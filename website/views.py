from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Note

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:  # Check if the user is admin
            records = Note.objects.all()  # Fetch all records for admin
        else:
            records = Note.objects.filter(user=request.user)  # Fetch records for normal users
        return render(request, 'home.html', {"records": records})
    else:
        return redirect('login')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
			# Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})



def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up records
        customer_record = Note.objects.get(id=pk)
        return render(request, 'record.html', {"customer_record": customer_record})
    else:
        messages.success(request, "You must be log in to veiw this page....")
        return redirect("home")
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Note.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "You have deleted the record....")
        return redirect("home")
    else:
        messages.success(request, "You must be logged in to do that....")
        return redirect("home")
@login_required
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid:
                add_record = form.save(commit=False)
                add_record.user = request.user
                add_record.save()
                messages.success(request, "Record Aadded....")
                return redirect("home")
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to do that....")
        return redirect("home")




def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Note.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():  # Add parentheses to is_valid method
            form.save()
            messages.success(request, "Record updated successfully.")
            return redirect("home")
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to update records.")
        return redirect("home")

    
    