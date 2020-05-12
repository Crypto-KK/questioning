from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    slug_field = "username"
    slug_url_kwarg = "username"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """自己信息"""
    model = User
    fields = ["nickname", 'email', 'picture', 'introduction', 'job_title',
              'personal_url', 'location']
    template_name = 'users/user_form.html'

    def get_success_url(self):
        """更新成功后跳转"""
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


