from django import forms

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
