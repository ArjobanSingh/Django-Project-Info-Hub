from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import PostUpdateForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .models import Post
from accounts.models import Profile


'''class BlogListView(ListView):
    model = Post
    paginate_by = 2
    ordering = ['-id']
    template_name = 'blog/home.html' '''

def blog_list(request):
    posts_list = Post.objects.all().order_by('-id')    
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/home.html', {'posts': posts})

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'   

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_new.html'
    fields = ['title', 'body']     

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BlogCreateView, self).form_valid(form)

"""class BlogUpdateView(LoginRequiredMixin,UserPassesTextMixin, UpdateView):
    model=Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'body']    

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user """
    

@login_required
def blog_update(request, pk):
    try:
        required_object = Post.objects.get(pk=pk)
        if request.method == 'POST':
            if request.user != required_object.author:
                return render(request, 'blog/error.html', {'error': "You are not the original author of this Post "})
            form = PostUpdateForm(request.POST, instance=required_object)
            if form.is_valid():
                form.save()
                return redirect(reverse('post_detail', args=[str(pk)]))
        else:        
            form = PostUpdateForm(instance= required_object)
            if request.user != required_object.author:
                return render(request, 'blog/error.html', {'error': "You are not the original author of this Post "})
            return render(request, 'blog/post_edit.html',{'form': form})
    except:    
        raise Http404("Page does not exist")


"""class BlogDeleteView(LoginRequiredMixin, UserPassesTextMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')    
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.author"""


@login_required
def blog_delete(request, pk):
    try:
        required_object = Post.objects.get(pk=pk)
        if request.method == 'POST':
            if request.user != required_object.author:
                return render(request, 'blog/error.html', {'error': "You are not the original author of this Post "})
            required_object.delete()
            return redirect('home')
        else:        
            if request.user != required_object.author:
                return render(request, 'blog/error.html', {'error': "You are not the original author of this Post "})
            return render(request, 'blog/post_delete.html', {'post': required_object})
    except:    
        raise Http404("Page does not exist")


@login_required
def following_posts(request):
    follower = request.user.profile

    # query all profiles which are followed by this(logged in user) follower profile 
    following = Profile.objects.filter(followed_by=follower)

    users= User.objects.filter(profile__in=following)
    posts = Post.objects.filter(author__in=users)
    return render(request, 'blog/following_posts.html', {'posts': posts, 'count': posts.count()})         

