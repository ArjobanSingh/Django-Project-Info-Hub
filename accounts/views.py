from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.shortcuts import render, reverse, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode

from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm, ProfileBioEditForm, ProfilePicEditForm
from django.contrib import messages
from .models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Post
# Create your views here.

#class SignUpView(generic.CreateView):
    #form_class = UserRegisterForm
    #success_url = reverse_lazy('login')
    #template_name = 'accounts/signup.html'

def registration(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()

            #creating profile for new registered user
            Profile.objects.create(user=new_user)

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })

            new_user.email_user(subject, message)
            return redirect('account_activation_sent')
            
            
    else:
        if request.user.is_authenticated:
            return redirect('home')
        form = UserRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})  

def account_activation_sent(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/activation_sent.html')       

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirm = True
        user.profile.save()
        user.save()

        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/account_activation_invalid.html')           

@login_required
def user_profile(request, pk):
    user_profile = Profile.objects.get(pk=pk)
    user = user_profile.user
    if request.method == "POST":
        bio_form = ProfileBioEditForm(request.POST, instance=user_profile)  
        pic_form = ProfilePicEditForm(request.POST, request.FILES, instance=user_profile)
        if bio_form.is_valid():
            bio_form.save()
        if pic_form.is_valid():
            pic_form.save()
        return redirect(reverse('profile', args=[pk]))    
    else:        
        bio_form = ProfileBioEditForm(instance=user_profile)  
        pic_form = ProfilePicEditForm(instance=user_profile) 
    user_posts = Post.objects.filter(author=user).order_by('-id')  
    paginator = Paginator(user_posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    followers = user_profile.followed_by.count()
    following = user_profile.follows.count()
    # follower_list = []
    # following_list = []
    # for follower in user_profile.followed_by.all():
    #     follower_list.append(follower)
    # for follow in user_profile.follows.all():
    #     following_list.append(follow)     
    is_follower = False
    if request.user.profile in user_profile.followed_by.all():
        is_follower = True    
    return render(request, 'accounts/profile.html', {'followers': followers, 
                                                    'following': following, 
                                                    'user_profile': user_profile, 
                                                    'follower_list': user_profile.followed_by.all(),
                                                    'following_list': user_profile.follows.all(),
                                                    'is_follower': is_follower, 
                                                    'this_user': request.user.profile.id,
                                                    'bio_form': bio_form, 'pic_form': pic_form,
                                                    'user_posts': posts})

@login_required
def follow_user(request, pk):
    if request.method == "POST":
        follow_user_profile = Profile.objects.get(pk=pk)
        if request.user != follow_user_profile.user:
            follower = request.user
            if follower.profile not in follow_user_profile.followed_by.all():
                follower.profile.follows.add(follow_user_profile)
                return JsonResponse({'done': True})
            else:
                follower.profile.follows.remove(follow_user_profile)    
                return JsonResponse({'done': False})    
            #return redirect(reverse('profile', args=[pk]))

