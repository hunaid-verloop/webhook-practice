from common.webhooker import WebHooker
from common.datastructures import section, action, list_item
from local_services.gsheetpractice.gsheet_utills import GsheetPracticeUtils

import settings
import logging
from verloop.utils.logger import get_logger
from utils.gsheets_client import GSheetsService
from common.exceptions import NoContentException
import ast


class Bot(WebHooker):
    def __init__(self):
        super(Bot, self).__init__()
        self._client = "gsheetpractice"
        self.gsheet_utils = GsheetPracticeUtils(
            settings.GDRIVE_SCOPE, settings.GDRIVE_CRED
        )

    def Fetch_Rooms(self, *args, visitor, variables, context, **kwargs):
        city_entered = variables.get("city_hunaidgsheetpractice", {}).get("parsed_value", "")
        area_entered = variables.get("area_hunaidgsheetpractice", {}).get("parsed_value", "")
        rooms = self.gsheet_utils.get_rooms(context)

        print(type(rooms))
        print(type(rooms[0]))
        print(rooms[0])

        rooms_available = []
        for r in rooms:
            agent_data = ast.literal_eval(r['Room'])

            if r['City'] == city_entered and r['Area'] == area_entered:
                rooms_available.append(
                    list_item(
                        title=agent_data['name'],
                        subtitle=agent_data['phone'],
                        action=action(
                            roomselected_hunaidgsheetpractice=f"Agent: {agent_data['name']} Phone: {agent_data['phone']} Rent: {agent_data['price']}",
                            next_block="Room_Details",
                        ),
                    )
                )
        room_list = [section(title="Select a room", items=rooms_available)]
        self.export(RoomList=room_list)
        self.next_block(name="Rooms")

