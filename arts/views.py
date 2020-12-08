from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from arts.forms.art_form import ArtForm
from arts.forms.comment_form import CommentForm
from arts.models import Art, Like, Comment
from core.GroupRequiredMixin import GroupRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class ArtListView(ListView):
    context_object_name = 'arts'
    model = Art
    template_name = 'art_list.html'


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


class ArtCreateView(GroupRequiredMixin, CreateView, LoginRequiredMixin, ArtForm):
    model = Art
    form_class = ArtForm
    groups = ['Regular User']
    template_name = 'art_create.html'
    success_url = reverse_lazy('list arts')


class ArtEditView(GroupRequiredMixin, UpdateView, LoginRequiredMixin, ArtForm):
    model = Art
    form_class = ArtForm
    groups = ['Regular User']
    template_name = 'art_edit.html'
    success_url = reverse_lazy('list arts')


class ArtDeleteView(GroupRequiredMixin, DeleteView, LoginRequiredMixin):
    model = Art
    groups = ['Regular User']
    template_name = 'art_delete.html'
    success_url = reverse_lazy('list arts')


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
