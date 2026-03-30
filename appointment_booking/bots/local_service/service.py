from utils.api_client import APIClient

class {{ client_id }}Service(object):
    def __init__(self, base_url: str):
        self.api_client = APIClient(base_url=base_url)