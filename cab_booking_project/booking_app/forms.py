from django import forms
from booking_app.models import Bookings


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['username'].widget.attrs['required'] = True
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['password'].widget.attrs['placeholder'] = "Password"
        self.fields['password'].widget.attrs['required'] = True
        self.fields['password'].widget.attrs['class'] = 'form-control'

    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30, required=True)


class SignUpForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['username'].widget.attrs['required'] = True
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['email'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = "Phone Number"
        self.fields['phone'].widget.attrs['required'] = True
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = "Password"
        self.fields['password'].widget.attrs['required'] = True
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['repeatpassword'].widget.attrs['placeholder'] = "Repeat Password"
        self.fields['repeatpassword'].widget.attrs['required'] = True
        self.fields['repeatpassword'].widget.attrs['class'] = 'form-control'

    username = forms.CharField(label="UserName", max_length=32)
    email = forms.CharField(label="Email", max_length=32, widget=forms.EmailInput)
    phone = forms.CharField(max_length=15)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    repeatpassword = forms.CharField(max_length=32, widget=forms.PasswordInput)


class BookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['return_date_time'].required = False

    class Meta:
        model = Bookings
        fields = ['depart_city', 'destination_city', 'depart_date_time', 'return_date_time', 'driver', 'price']


class ContactDetailForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['username'].widget.attrs['required'] = True
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['email'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = "Phone Number"
        self.fields['phone'].widget.attrs['required'] = True
        self.fields['phone'].widget.attrs['class'] = 'form-control'

    username = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=32, widget=forms.EmailInput())
    phone = forms.CharField(max_length=30)

