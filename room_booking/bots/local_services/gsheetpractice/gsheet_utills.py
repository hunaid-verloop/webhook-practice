from verloopcontext.context import Context
from gspread.models import Spreadsheet, Worksheet

from utils.gsheets_client import GSheetsService


class GsheetPracticeUtils(object):
    def __init__(self, scope: str, creds: str) -> None:
        self._gsheet_scope = scope
        self._gsheet_creds = creds

    def _get_google_sheet(self, sheet_name: str, context: Context) -> Spreadsheet:
        """
        Initializing the google spreadsheet
        """

        LOGGER = context.get_logger()
        ss = GSheetsService(self._gsheet_scope, self._gsheet_creds)
        data = ss.get_sheet(context, sheet_name=sheet_name)
        LOGGER.info("Gsheets all sheet data", gsheet_data=data)
        return data

    def get_worksheet(
        self, sheet_name: str, worksheet_name: str, context: Context
    ) -> Worksheet:
        """
        Get worksheet object
        """

        LOGGER = context.get_logger()
        gsheet_obj = self._get_google_sheet(sheet_name=sheet_name, context=context)
        worksheet = gsheet_obj.worksheet(worksheet_name)
        LOGGER.info("Worksheet all data", worksheet_data=worksheet)
        return worksheet

    def get_rooms(self, context: Context) -> list:
        """
        Get list of data of all stores
        """
        LOGGER = context.get_logger()
        rooms = []
        try:
            worksheet = self.get_worksheet(
                sheet_name="myclient",
                worksheet_name="rrms",
                context=context,
            )
        except:
            LOGGER.error("Error in fetching stores from GShseet", exc_info=True)
            return rooms

        worksheet_data = worksheet.get_all_values()
        keys = worksheet_data[0]

        for single_data in worksheet_data[1:]:
            final_data = dict(zip(keys, single_data))
            rooms.append(final_data)

        # LOGGER.info("Room list from GSheet", rooms_data=rooms)
        return rooms
