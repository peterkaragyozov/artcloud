from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins

from artcloud.arts.forms.art_form import ArtForm
from artcloud.arts.forms.comment_form import CommentForm
from artcloud.arts.models import Art, Like, Comment
from artcloud.core.GroupRequiredMixin import GroupRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View, FormView

from artcloud.core.clean_up import clean_up_files


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


class ArtCreateView(auth_mixins.LoginRequiredMixin, CreateView):
    template_name = 'art_create.html'
    model = Art
    form_class = ArtForm

    def get_success_url(self):
        url = reverse_lazy('art details', kwargs={'pk': self.object.id})
        return url

    def form_valid(self, form):
        art = form.save(commit=False)
        art.user = self.request.user.userprofile
        art.save()
        return super().form_valid(form)


class ArtEditView(auth_mixins.LoginRequiredMixin, UpdateView):
    template_name = 'art_edit.html'
    model = Art
    form_class = ArtForm

    def get_success_url(self):
        url = reverse_lazy('art details', kwargs={'pk': self.object.id})
        return url

    def form_valid(self, form):
        old_image = self.get_object().image
        if old_image:
            clean_up_files(old_image.path)
        return super().form_valid(form)


class ArtDeleteView(auth_mixins.LoginRequiredMixin, DeleteView):
    model = Art
    template_name = 'art_delete.html'
    success_url = reverse_lazy('list arts')

    def dispatch(self, request, *args, **kwargs):
        art = self.get_object()
        if art.user_id != request.user.userprofile.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


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
