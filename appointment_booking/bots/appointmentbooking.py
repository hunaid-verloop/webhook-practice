from settings import APPOINTMENT_BOOKING_BASE_URL
from local_services.appointmentbooking.service import AppointmentBookingService
from common.webhooker import WebHooker
from common.datastructures import card, quick_reply, list_item, postback, url, action
import datetime

class Bot(WebHooker):

    def __init__(self):
        super(Bot, self).__init__()
        self._client = "appointmentbooking"
        self.service = AppointmentBookingService(
            base_url=APPOINTMENT_BOOKING_BASE_URL,
        )

    def Get_Dates(self, *args, visitor, variables, **kwargs):
        date_requested = variables.get("date_appointmentbooking", {}).get("value", "")
        if not self._is_valid_date(date_requested):
            self.next_block(name="Invalid_Date")
            self.export(DateList=[])
            return

        # TODO make a request to the external api to get the dates around the variable "date_requested"
        dates_around = self.service.get_dates(date_requested)

        dates = [
            list_item(
                title=d,
                subtitle=" ",
                action=action(
                    dateselected_appointmentbooking=d,
                    next_block="Request_Duration",
                ),
            )
            for d in dates_around
        ]
        # self.next_block(name="Available_Dates")
        self.export(DateList=dates)

    def Get_Available_slots(self, *args, visitor, variables, **kwargs):
        date_requested = variables.get("date_appointmentbooking", {}).get("value", "")
        if not self._is_valid_date(date_requested):
            self.next_block(name="Invalid_Date")
            self.export(DateList=[])
            return
        
        duration_requested = variables.get("duration_appointmentbooking", {}).get("value", "")
        if not self._is_valid_duration(duration_requested):
            self.next_block(name="Invalid_Duration")
            self.export(SlotList=[])
            return
        
        # TODO make a request to the external api to get the dates around the variable "date_requested"
        available_slots = self.service.get_timeslots(duration_requested)      

        slots = [
            list_item(
                title=date_requested,
                subtitle=" ",
                action=action(
                    slotselected_appointmentbooking=s,
                    next_block="Book_Appointment",
                ),
            )
            for s in available_slots
        ]
        self.next_block(name="Available_Slots")
        self.export(SlotList=slots)

    def _is_valid_date(self, date_entered):
        try:
            # Check if it matches the exact format YYYY-MM-DD
            entered_date = datetime.strptime(date_entered, "%Y-%m-%d")
            today = datetime.datetime.now()
            
            return entered_date >= today and (entered_date-today < datetime.timedelta(days=365))
        except ValueError:
            return False
        
    def _is_valid_duration(self, duration_entered):
        return isinstance(duration_entered, int) and duration_entered <= 60
    

