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


class ArtDetailsView(DetailView):
    model = Art
    template_name = 'art_detail.html'
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art = context[self.context_object_name]
        context['form'] = CommentForm()
        context['can_delete'] = self.request.user == art.user.user
        context['can_edit'] = self.request.user == art.user.user
        context['can_like'] = self.request.user != art.user.user
        context['has_liked'] = art.like_set.filter(user_id=self.request.user.userprofile.id).exists()
        context['can_comment'] = self.request.user != art.user.user
        context['comments'] = list(art.comment_set.all())

        return context


class LikeArtView(View):
    def get(self, request, **kwargs):
        user_profile = request.user.userprofile
        art = Art.objects.get(pk=kwargs['pk'])

        like = art.like_set.filter(user_id=user_profile.id).first()
        if like:
            like.delete()
        else:
            like = Like(
                user=user_profile,
                art=art,
                test='as'
            )
            like.save()

        return redirect('art details', art.id)


class CommentArtView(auth_mixins.LoginRequiredMixin, FormView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user.userprofile
        comment.art = Art.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return redirect('art details', self.kwargs['pk'])


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
        if old_image and old_image != form.cleaned_data['image']:
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
