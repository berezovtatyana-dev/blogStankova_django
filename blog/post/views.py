from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm, CommentForm

from .models import Post, Comment

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
        'page_title': 'Все посты блога'
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        # проверка на авторизацию свойство is_authenticated
        if not request.user.is_authenticated:
            messages.warning(request, 'Авторизуйтесь, чтобы оставить комментарий')
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) #commit - сохраняет данные в БД
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect('post:post_detail', post_id=post.id)
        else:
            messages.error(request, 'Ошибка при добавлении комментария')
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'page_title': post.title
    }
    return render(request, 'post/post_details.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост создан')
            return redirect('post:post_detail', post_id=post.id)
        else:
            messages.error(request, 'Ошибка в форме')
    else:
        form = PostCreateForm()
    context = {
        'form': form,
        'page_title': 'Создание нового поста',
    }
    return render(request, 'post/post_create.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        # instance отвечает за передачу значений свойств объекта
        form = PostCreateForm(request.POST, instance=post)
f       if form.is_valid():
            form.save()
            messages.success(request, 'Пост обновлен')
            return redirect('post:post_detail', post_id=post.id)
        else:
            messages.error(request, 'Ошибка в форме при обновлении')
    else:
        form = PostCreateForm(instance=post)
    context = {
        'form': form,
        'post': post,
        'page_title': f'Редактирование {post.title}',
    }
    return render(request, 'post/post_edit.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            post.delete()
            messages.success(request, 'Пост удален')
            return redirect('post:post_list')
        else:
            return redirect('post:post_detail', post_id=post.id)
    comments = post.comments.all().order_by('-created_at')
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form'form,
        'delete_confirm': True, #Флаг для отображения кнопки
        'page_title': f'Удаление {post.title}',
    }
    return render(request, 'post/post_detail.html', context)
