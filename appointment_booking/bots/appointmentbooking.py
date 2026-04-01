from settings import APPOINTMENT_BOOKING_BASE_URL
from local_services.appointmentbooking.service import AppointmentBookingService
from common.webhooker import WebHooker
from common.datastructures import card, quick_reply, list_item, postback, url, action, section
from datetime import datetime, timedelta

class Bot(WebHooker):

    def __init__(self):
        super(Bot, self).__init__()
        self._client = "appointmentbooking"
        self.service = AppointmentBookingService(
            base_url=APPOINTMENT_BOOKING_BASE_URL,
        )

    def Get_Dates(self, *args, visitor, variables, context, **kwargs):
        date_requested = variables.get("date_appointmentbooking", {}).get("value", "")
        if not self._is_valid_date(date_requested):
            self.next_block(name="Invalid_Date")
            self.export(DateList=[])
            return

        dates_around = self.service.get_dates(date_requested, context)

        dates = [
            list_item(
                title=d,
                subtitle=" ",
                action=action(
                    dateselected_appointmentbooking=d,
                    next_block="Request_Duration",
                ),
            )
            for d in dates_around.get("dates_around_requested_date", [])
        ]
        date_list = [section(title="Select a date", items=dates)]
        self.next_block(name="Available_Dates")
        self.export(DateList=date_list)

    def Get_Available_Slots(self, *args, visitor, variables, context, **kwargs):
        date_selected = variables.get("dateselected_appointmentbooking", {}).get("parsed_value", "")
        if not self._is_valid_date(date_selected):
            self.next_block(name="Invalid_Date")
            self.export(DateList=[])
            return
        
        duration_requested = variables.get("duration_appointmentbooking", {}).get("parsed_value", 0)
        if not self._is_valid_duration(duration_requested):
            self.next_block(name="Invalid_Duration")
            self.export(SlotList=[])
            return
        
        print(f"date_selected: {date_selected} duration_requested: {duration_requested}")

        available_slots = self.service.get_timeslots(date_selected, duration_requested, context)
        print(available_slots)

        slots = [
            list_item(
                title=f"On {date_selected}",
                subtitle=s,
                action=action(
                    slotselected_appointmentbooking=s,
                    next_block="Book_Appointment",
                ),
            )
            for s in available_slots.get('available_timeslots', [])
        ]
        slot_list = [section(title="Select a time slot", items=slots)]
        self.next_block(name="Available_Slots")
        self.export(SlotList=slot_list)

    def Book_Appointment(self, *args, visitor, variables, context, **kwargs):
        date_selected = variables.get("dateselected_appointmentbooking", {}).get("parsed_value", "")
        if not self._is_valid_date(date_selected):
            self.next_block(name="Invalid_Date")
            self.export(DateList=[])
            return
        
        slot_requested = variables.get("slotselected_appointmentbooking", {}).get("parsed_value", "")

        resp = self.service.do_booking(date_selected, slot_requested, context)

        self.next_block(name="Confirmed")
        variables["message_appointmentbooking"] = resp.get("message", "")


    def _is_valid_date(self, date_entered):
        try:
            # Check if it matches the exact format YYYY-MM-DD
            entered_date = datetime.strptime(date_entered, "%Y-%m-%d")
            today = datetime.now()
            
            return True if (today - entered_date) == timedelta(days=0) else (entered_date - today < timedelta(days=365))
        except ValueError:
            return False
        
    def _is_valid_duration(self, duration_entered):
        return isinstance(duration_entered, int) and duration_entered <= 60
    

