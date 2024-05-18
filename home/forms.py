from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        service_provider = self.instance.service_provider
        product = self.instance.product

        if date and time and service_provider:
            booking_start = datetime.combine(date, time)
            booking_end = booking_start + timedelta(hours=1)

            conflicting_bookings = Booking.objects.filter(
                service_provider=service_provider,
                product=product,
                date=date,
                time__gte=(booking_start - timedelta(hours=1)).time(),
                time__lt=(booking_end).time(),
            ).exclude(pk=self.instance.pk) 

            if conflicting_bookings.exists():
                raise ValidationError("This time slot is already booked for this service. Please choose another time.")

        return cleaned_data
