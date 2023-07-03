from django.shortcuts import render
from hotel.views import RoomListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import ContactForm

class HomePage(RoomListView):
    template_name = 'content_app/index.html'

class ContactView(FormView):
    template_name = 'content_app/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('content_app:home')

    def form_valid(self, form):
        # Save the message in the database
        form.save()

        # Send the email
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        # Prepare the email data
        email_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }

        # Send the email to the specified destination email
        send_mail(
            f'New Contact Message - {subject}',
            '',
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            html_message=render_to_string('contact_mail/contact_message.html', email_data),
        )

        # Send email to the user
        user_email_data = {
            'name': name,
            'email': email,
        }

        send_mail(
            'Thank you for contacting us',
            '',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=render_to_string('contact_mail/contact_user.html', user_email_data),
        )

        return super().form_valid(form)


