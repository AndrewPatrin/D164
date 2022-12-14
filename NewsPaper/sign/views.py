from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import BaseRegisterForm
from newsportal.models import Author

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/personal.html'


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request, "Your email is confirmed. Account is activated.")
        return redirect('/sign/login/')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('/sign/login/')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("account/email/email_confirmation_massage.html", {
        'user': user.username,
        'domain': get_current_site(request).domain + ':8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Hello <b>{user}</b>, please go to you email <b>{to_email}</b> and click on \
                received activation link to confirm and complete the registration.')
    else:
        messages.error(
            request, f'Sending email to {to_email} failed, check if you typed it correctly.')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/login/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        activateEmail(self.request, user, form.cleaned_data['email'])
        return super().form_valid(form)

    """
    def form_valid(self, form):
        user = form.save(commit=False)
        try:
            return super().form_valid(form)
        finally:
            basic_group = Group.objects.get(name='common')
            basic_group.user_set.add(user)
    """


@login_required
def set_user_group_to_common(request):
    user = request.user
    common_group = Group.objects.get(name='common')
    if not request.user.groups.filter(name='common').exists():
        common_group.user_set.add(user)
    return redirect('/account/')


@login_required
def set_user_group_author(request):
    user_cur = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user_cur)
    Author.objects.create(user=user_cur)
    return redirect('/account/')
