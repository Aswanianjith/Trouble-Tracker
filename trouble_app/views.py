import logging
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Issue
from .forms import CustomUserCreationForm, IssueForm, CommentForm
from django.db import IntegrityError
from django.http import HttpResponseForbidden

# Set up logging configuration
logging.basicConfig(
    filename='dashboard.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example view to fetch all issues and print SQL queries executed
@login_required
def some_view(request):
    issues = Issue.objects.all()
    logging.info(f"SQL queries executed: {len(connection.queries)}")
    return render(request, 'template.html', {'issues': issues})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    issues = Issue.objects.all()
    return render(request, 'index.html', {'issues': issues})

@login_required
def my_view(request):
    return redirect('dashboard')

class IssueUpdateView(PermissionRequiredMixin, UpdateView):
    model = Issue
    fields = ['title', 'description', 'priority', 'assigned_to', 'status']
    template_name_suffix = '_update_form'
    permission_required = 'myapp.change_issue'  # Ensure 'myapp' matches your app name

    def form_valid(self, form):
        issue = form.save(commit=False)
        if issue.status == 'Resolved':
            issue.resolved_by = self.request.user
        issue.save()
        return super().form_valid(form)

@login_required
def issue_list(request):
    query = request.GET.get('q')
    if query:
        issues = Issue.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(status__icontains=query) |
            Q(priority__icontains=query) |
            Q(assigned_to__username__icontains=query)
        )
    else:
        issues = Issue.objects.all()
    
    return render(request, 'issue_list.html', {'issues': issues})

@login_required
def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.issue = issue
            comment.author = request.user
            comment.save()
            return redirect('issue_detail', issue_id=issue_id)
    return render(request, 'issue_detail.html', {'issue': issue, 'comment_form': comment_form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Replace 'home' with your actual redirect URL after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            try:
                new_issue = form.save(commit=False)
                new_issue.created_by = request.user
                new_issue.save()
                return redirect('issue_list')
            except IntegrityError as e:
                # Handle the IntegrityError due to duplicate entry
                form.add_error(None, "An issue with this title already exists.")
        # If form is invalid, or IntegrityError occurred, render the form again
        return render(request, 'create_issue.html', {'form': form})
    else:
        form = IssueForm()
    
    return render(request, 'create_issue.html', {'form': form})
@login_required
def dashboard(request):
    logging.info(f"User '{request.user.username}' accessed the dashboard.")
    return render(request, 'dashboard.html', {'username': request.user.username})

@login_required
def issue_edit(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Issue updated successfully!')
            return redirect('issue_list')
    else:
        form = IssueForm(instance=issue)
    return render(request, 'issue_form.html', {'form': form})


@login_required
def create_confirm_delete(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    if request.method == "POST":
        if issue.created_by != request.user:
            return HttpResponseForbidden("You are not allowed to delete this issue.")
        issue.delete()
        return redirect(reverse('issue_list'))
    return render(request, 'create_confirm_delete.html', {'issue_id': issue_id})