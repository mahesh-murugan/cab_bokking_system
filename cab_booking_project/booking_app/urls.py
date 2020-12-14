from django.conf.urls import url
from booking_app.views import HomeView, jsonreader, CabConfirmView, CabBookingReView, LoginView, SignUpView, \
    CabBookingConfirmationView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login_view"),
    url(r'^signup/$', SignUpView.as_view(), name="signup_view"),
    url(r'^home/$', HomeView.as_view(), name="home_view"),
    url(r'^json/(?P<filename>[.\w]+)/$', jsonreader, name="json_reader_view"),
    url(r'^cabs/(?P<id>[\d]+)/$', CabConfirmView.as_view(), name="cab_confirm_view"),
    url(r'^cab/(?P<id>[\d]+)/review/$', CabBookingReView.as_view(), name="cab_booking_review_view"),
    url(r'^cab/booked/$', CabBookingConfirmationView.as_view(), name="cab_booked_view"),
]
