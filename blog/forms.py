from django.forms import ModelForm
from .models import Post

# Create the form class.
class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']