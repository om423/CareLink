class MapsClient:
    """Placeholder Google Maps client. Do not call external APIs here yet."""
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def search_nearby(self, query: str, lat: float, lng: float) -> list[dict]:
        raise NotImplementedError("Not implemented: placeholder only.")

