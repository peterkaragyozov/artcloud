from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from accounts.decorators import user_required
from arts.forms.art_form import ArtForm
from arts.forms.comment_form import CommentForm
from arts.models import Art, Like, Comment
from core.clean_up import clean_up_files


def list_arts(request):
    context = {
        'arts': Art.objects.all(),
    }

    return render(request, 'art_list.html', context)


@login_required
def details_or_comment_art(request, pk):
    art = Art.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'art': art,
            'form': CommentForm(),
            'can_edit': request.user == art.user.user,
            'can_delete': request.user == art.user.user,
            'can_like': request.user != art.user.user,
            'has_liked': art.like_set.filter(user_id=request.user.userprofile.id).exists(),
            'can_comment': request.user != art.user.user,
        }

        return render(request, 'art_detail.html', context)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(text=form.cleaned_data['text'])
            comment.art = art
            comment.user = request.user.userprofile
            comment.save()
            return redirect('art details or comment', pk)
        context = {
            'art': art,
            'form': form,
        }

        return render(request, 'art_detail.html', context)


def persist_art(request, art, template_name):
    if request.method == 'GET':
        form = ArtForm(instance=art)

        context = {
            'form': form,
            'art': art,
        }

        return render(request, f'{template_name}.html', context)
    else:
        old_image = art.image
        form = ArtForm(
            request.POST,
            request.FILES,
            instance=art
        )
        if form.is_valid():
            if old_image:
                clean_up_files(old_image.path)
            form.save()
            Like.objects.filter(art_id=art.id).delete()

            return redirect('art details or comment', art.pk)

        context = {
            'form': form,
            'art': art,
        }

        return render(request, f'{template_name}.html', context)


@login_required
def create_art(request):
    art = Art()
    return persist_art(request, art, 'art_create')


@user_required(Art)
def edit_art(request, pk):
    art = Art.objects.get(pk=pk)
    return persist_art(request, art, 'art_edit')


@login_required
def delete_art(request, pk):
    art = Art.objects.get(pk=pk)
    if art.user.user != request.user:
        # forbid
        pass

    if request.method == 'GET':
        context = {
            'art': art,
        }

        return render(request, 'art_delete.html', context)
    else:
        art.delete()
        return redirect('list arts')


@login_required
def like_art(request, pk):
    like = Like.objects.filter(user_id=request.user.userprofile.id, art_id=pk).first()
    if like:
        like.delete()
    else:
        art = Art.objects.get(pk=pk)
        like = Like(test=str(pk), user=request.user.userprofile)
        like.art = art
        like.save()
    return redirect('art details or comment', pk)
