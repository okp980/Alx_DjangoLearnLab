from django.shortcuts import render
from .forms import RegisterForm, ProfileForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from blog.models import Post

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/list_posts.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'