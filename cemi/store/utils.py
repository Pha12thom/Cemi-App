# utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your account.'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activation_url = f"{request.scheme}://{request.get_host()}{activation_link}"
    message = render_to_string('activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })
    send_mail(mail_subject, message, 'geofreymilugo@gmail.com', [to_email])
