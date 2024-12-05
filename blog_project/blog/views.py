import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.i18n import set_language
from .models import Post, Category
from .forms import PostForm, RegisterForm
## importer count pour pouvoir compter la liste des artocles
from django.db.models import Count
## importer  jsonresponse pour les favoris
from django.http import JsonResponse
logger = logging.getLogger('blog')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f'{_("New user registered")}: {user.username}')
            messages.success(request, _('Account created successfully!'))
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def post_list(request):
    posts = Post.objects.all().select_related('author', 'category')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories
    })

def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related('author', 'category'), slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, _('Post created successfully!'))
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        messages.error(request, _("You don't have permission to edit this post"))
        return redirect('post_detail', slug=slug)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, _('Post updated successfully!'))
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        messages.error(request, _("You don't have permission to delete this post"))
        return redirect('post_detail', slug=slug)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, _('Post deleted successfully!'))
        return redirect('post_list')
    return render(request, 'blog/post_delete.html', {'post': post})

def logout_view(request):
    logout(request)
    messages.success(request, _('You have been logged out successfully.'))
    return redirect('post_list')


#Vues pour les catégories 

def category_list(request):#pour afficher toutes les catégories
    
    # Utilisation de 'annotate' pour compter le nombre d'articles (posts) par catégorie
    categories = Category.objects.annotate(num_posts=Count('posts'))
    return render(request, 'category/category_list.html', {
        'categories': categories
    })
# pour afficher les détails de la catégorie
def category_detail(request, slug):
    # Récupère la catégorie en fonction de son slug
    category = get_object_or_404(Category, slug=slug)

    # Récupère tous les articles associés à cette catégorie
    posts = category.posts.all()  # Utilisation du 'related_name' 'posts' défini dans Post relation one2many
    
    return render(request, 'category/category_detail.html', {'category': category, 'posts': posts})

#ajout de la fonction favoris avec uniquement si l'utilisateur est connectet
@login_required
def function_make_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Inverser l'état de is_favorite
    
    post.is_favorite = not post.is_favorite
    # sauvegarder
    post.save()

    return JsonResponse({'is_favorite': post.is_favorite})

     