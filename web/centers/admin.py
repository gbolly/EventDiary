from django.contrib import admin
from .models import Center, Booking, State, LocalGovArea


class BookingModelAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'booking_start_date', 'booking_end_date', 'phone_number', 'is_approved']
    list_filter = ['is_approved', 'booking_start_date']
    search_fields = ['customer_name']
    list_editable = ['is_approved', 'phone_number']

    actions = ['email_customers']

    def email_customers(self, request, queryset):
        for booking in queryset:
            if booking.is_approved:
                email_body = """Dear {},
    We are pleased to inform you that your booking has been approved.
Thanks
""".format(booking.customer_name)
            else:
                email_body = """Dear {},
    Unfortunately we do not have the capacity right now to accept your booking.
Thanks
""".format(booking.customer_name)

            print(email_body)
            self.message_user(request, 'Emails were send successfully')
    email_customers.short_description = 'Send email about booking status to customers'

admin.site.register(Center)
admin.site.register(Booking, BookingModelAdmin)
admin.site.register(State)
admin.site.register(LocalGovArea)
