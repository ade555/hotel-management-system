from django.shortcuts import render
from hotel.views import RoomListView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import ContactForm
from .models import TouristSpot

# this view from the homepage inherits from the hotel.RoomListView view in the hotel app
class HomePage(RoomListView):
    template_name = 'content_app/index.html'

class AboutPage(TemplateView):
    template_name = 'content_app/about.html'

class TouristPage(ListView):
    template_name = 'content_app/tourist.html'
    context_object_name = 'tourist_places'
    model = TouristSpot

# contact view for user to send feedback and make enquires
class ContactView(FormView):
    template_name = 'content_app/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('content_app:contact')

    # if the form is valid, save the message to the model, send an email to the user and an admin email specified.
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

        messages.success(self.request, 'Your message has been sent successfully!')

        return super().form_valid(form)


