from django import forms
from project_core.utils import DivErrorList

# create a form that accepts the check-in and check-out date from the user. this will be used to book a room
class BookingForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'})
    )
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = DivErrorList