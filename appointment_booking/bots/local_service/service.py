from local_services.appointmentbooking.client import AppointmentBookingClient


class AppointmentBookingService(object):

    def __init__(self, base_url):
        self.client = AppointmentBookingClient(base_url=base_url)

    def get_dates(self, date_requested, context):
        data = {
           "date_requested": date_requested
        }
        response = self.client._get_dates(data=data, context=context)
        return response.get('status', {})

    def get_timeslots(self, date_requested, duration_requested, context):
        data = {
            "date_requested": date_requested,
            "duration_requested_minutes": duration_requested
        }
        response = self.client._get_timeslots(data=data, context=context)
        return response.get('status', {})

    def do_booking(self, date_requested, time_slot, context):
        data = {
            "date": date_requested,
            "time_slot": time_slot
        }
        response = self.client._do_booking(data=data, context=context)
        return response.get('status', {})
