from common.webhooker import WebHooker
import random

class Bot(WebHooker):

    def __init__(self):
        super(Bot, self).__init__()
        self._client = "hotelbooking"

    def Book_Stay(self, *args, visitor, variables, context, **kwargs):
        startdate_selected = variables.get("startdate_hunaidhotelbooking", {}).get("parsed_value", "")
        enddate_selected = variables.get("enddate_hunaidhotelbooking", {}).get("parsed_value", "")
        room = get_available_room(startdate_selected, enddate_selected)
        self.next_block(name="Confirmed")
        variables["roombooked_hunaidhotelbooking"] = room

def get_available_room(startdate_selected, enddate_selected):
    floor = str(random.randint(1, 5))
    room_number = str(random.randint(1,13))
    sp = "0" if room_number < 10 else ""
    room = floor + sp + room_number
    return room

    

