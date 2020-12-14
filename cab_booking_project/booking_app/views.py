from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import datetime
import json

from booking_app.models import Bookings, Drivers, Profile
from booking_app.forms import BookingForm, LoginForm, SignUpForm, ContactDetailForm


class RedirectToHomeView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'home_view'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)


class LoginView(FormView):
    template_name = "booking_app/login/login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # logout if user already logged in
            print("logging out current user")
            logout(request)
        return render(request, self.template_name, context=self.get_context_data())

    def form_valid(self, form):
        if self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=name, password=password)
                if user is not None:
                    login(self.request, user=user)  # save user to session to access inner pages
                    return HttpResponseRedirect(reverse('home_view'))
            context = self.get_context_data()
            context['error'] = 'Username or Password invalid!!'
            return render(self.request, self.template_name, context=context)
        return super().form_valid(form)


class SignUpView(FormView):
    template_name = "booking_app/signup/signup.html"
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # logout if user already logged in
            print("logging out current user")
            logout(request)
        return render(request, self.template_name, context=self.get_context_data())

    def form_valid(self, form):
        if self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                phone = form.cleaned_data.get('phone')
                password = form.cleaned_data.get('password')
                repeatpassword = form.cleaned_data.get('repeatpassword')
                if password == repeatpassword:
                    user = User.objects.filter(username=username).first()
                    if user is not None:
                        context = self.get_context_data()
                        context['error'] = 'User already exists!!'
                        return render(self.request, self.template_name, context=context)
                else:
                    context = self.get_context_data()
                    context['error'] = 'Sorry, password entered is not matching'
                    return render(self.request, self.template_name, context=context)
                if username is not None:
                    if password == repeatpassword:
                        user = User()
                        user.username = username
                        user.email = email
                        user.password = make_password(password)
                        user.save()
                        user_id = User.objects.filter(id=user.id).first()

                        profile = Profile()
                        profile.user = user_id
                        profile.phone = phone
                        profile.save()
                        context = self.get_context_data()
                        context['success'] = 'Registration Completed Successfully!!'

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(self.request, user=user)  # save user to session to access inner pages
                    return HttpResponseRedirect(reverse('home_view'))
            context = self.get_context_data()
            context['error'] = 'Username or Password invalid!!'
            return render(self.request, self.template_name, context=context)
        return super().form_valid(form)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "booking_app/home/home.html"

    def get(self, request, *args, **kwargs):
        Bookings.objects.filter(customer=None).delete()
        return render(request, self.template_name)

    def post(self, request):
        if self.request.method == 'POST':
            origin_city = request.POST.get('origin_city', None)
            destination_city = request.POST.get('destination_city', None)
            depart_date_time = request.POST.get('depart_date_time', None)
            return_date_time = request.POST.get('return_date_time', None)
            round_trip_check = request.POST.get('round_trip_check', None)
            print(origin_city, destination_city, depart_date_time, return_date_time, round_trip_check)

            booking_obj = Bookings()
            booking_obj.depart_city = origin_city
            booking_obj.destination_city = destination_city
            booking_obj.depart_date_time = datetime.datetime.strptime(depart_date_time, "%d-%m-%Y %I:%M %p") \
                .strftime("%Y-%m-%d %H:%M:%S")
            if round_trip_check is not None:
                booking_obj.return_date_time = datetime.datetime.strptime(return_date_time, "%d-%m-%Y %I:%M %p") \
                    .strftime("%Y-%m-%d %H:%M:%S")
            booking_obj.save()

            return HttpResponseRedirect(reverse('cab_confirm_view', kwargs={'id': booking_obj.id}))
        return HttpResponseRedirect(reverse('home_view'))


def jsonreader(request, filename):
    data = {}
    if request.method == 'GET':
        try:
            file = open(filename, 'r')
            data['datas'] = json.loads(file.read())
        except Exception as e:
            print('Exception', e)
    return JsonResponse(data=data)


class CabConfirmView(LoginRequiredMixin, FormView):
    template_name = "booking_app/cabs/cabs.html"
    form_class = BookingForm

    def get_object(self):
        return Bookings.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super(CabConfirmView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        depart_city = self.get_object().depart_city
        destination_city = self.get_object().destination_city
        depart_date_time = self.get_object().depart_date_time
        return_date_time = self.get_object().return_date_time

        context['depart_city'] = depart_city
        context['destination_city'] = destination_city
        context['depart_date_time'] = depart_date_time.strftime("%d-%m-%Y %I:%M %P")

        if return_date_time is not None:
            context['return_date_time'] = return_date_time.strftime("%d-%m-%Y %I:%M %P")
        else:
            return_date_time = ''

        context['form'] = self.form_class(initial={
            'depart_city': depart_city,
            'destination_city': destination_city,
            'depart_date_time': depart_date_time,
            'return_date_time': return_date_time,
        })

        distance_kms = 0
        try:
            file = open('data.json', 'r')
            file = file.read()
            kms = json.loads(file)['{}_kms'.format(depart_city)]
            for city in kms:
                if destination_city in city:
                    distance_kms = city[destination_city]
        except Exception as e:
            print(e)

        context['distance_kms'] = distance_kms

        driver_list = []
        drivers_obj = Drivers.objects.filter(available_city=depart_city)
        for driver in drivers_obj:
            driver_list.append({
                'driver_id': driver.id,
                'driver_name': driver.name,
                'cab_name': driver.company_name,
                'car_type': driver.car_type,
                'car_name': driver.car_name,
                'language_known': driver.languages_known,
                'price_per_km': driver.price_per_km,
                'price': driver.price_per_km * distance_kms,
            })
        context['driver_list'] = json.dumps(driver_list)
        return render(request, self.template_name, context=context)

    def form_valid(self, form):
        if self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                driver = form.cleaned_data['driver']
                price = form.cleaned_data['price']
                booking_obj = self.get_object()
                booking_obj.driver = driver
                booking_obj.price = price
                booking_obj.save()
                return HttpResponseRedirect(reverse("cab_booking_review_view", kwargs={'id': booking_obj.id}))
        return HttpResponseRedirect(reverse("cab_confirm_view", kwargs={'id': self.get_object().id}))


class CabBookingReView(LoginRequiredMixin, FormView):
    template_name = "booking_app/review/review.html"
    form_class = ContactDetailForm

    def get_object(self):
        return Bookings.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        booking_obj = self.get_object()
        context['car_type'] = booking_obj.driver.car_type
        context['car_name'] = booking_obj.driver.car_name
        context['cab_name'] = booking_obj.driver.company_name
        context['trip_type'] = "Cab Two Way" if booking_obj.return_date_time is not None else "Cab One Way"
        context['pickup_time'] = booking_obj.depart_date_time.strftime("%a %d %b %Y %I:%M %P")
        context['from'] = booking_obj.depart_city
        context['to'] = booking_obj.destination_city
        context['price'] = booking_obj.price

        profile_obj = Profile.objects.filter(user=self.request.user).first()
        print(profile_obj.phone)
        context['form'] = self.form_class(initial={
            'username': self.request.user.username,
            'email': self.request.user.email,
            'phone': profile_obj.phone,
        })
        return context

    def form_valid(self, form):
        if self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                booking_obj = Bookings.objects.filter(id=self.get_object().id).first()
                if booking_obj is not None:
                    booking_obj.customer = self.request.user
                    booking_obj.save()
                    print('booking confirmed')
                    return HttpResponseRedirect(reverse('cab_booked_view'))
        return HttpResponseRedirect(reverse('cab_confirm_view', kwargs={'id': self.get_object().id }))


class CabBookingConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = "booking_app/confirm/confirm.html"

