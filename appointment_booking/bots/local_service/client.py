from verloop.utils.logger import get_logger
import requests
import json
import hashlib
import hmac

class AppointmentBookingClient(object):
    def __init__(self, base_url):
        self._base_url = base_url

    def _get_dates(self, data, context):
        return self._post(endpoint="/dates", data=data, context=context)

    def _get_timeslots(self, data, context):
        return self._post(endpoint="/availableslots", data=data, context=context)

    def _do_booking(self, data, context):
        return self._post(endpoint="/bookappointment", data=data, context=context)

    def _get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "verloop-io",
        }
        return headers

    def _post(self, endpoint, data, context, **headers):
        LOGGER = context.get_logger()
        url = self._base_url + endpoint
        print(url)
        LOGGER.info("Post request info for AppointmentBooking", **{"url": url, "data": data, "headers": self._get_headers(**headers)})
        resp = requests.post(url=url, data=json.dumps(
            data), headers=self._get_headers(**headers))
        LOGGER.info("Response for AppointmentBooking from client", **{"resp": resp.content, "status": resp.status_code})

        if resp.status_code != 200:
            raise Exception("Non 200 status received from abhibus APIs.")
        return resp.json()
