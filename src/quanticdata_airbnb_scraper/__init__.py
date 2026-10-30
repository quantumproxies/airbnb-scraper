"""Airbnb Scraper: Airbnb scraper for Python and the command line: stays for a city, region or neighbourhood with nightly price, stay total, rating, reviews, bedrooms, beds and map point, for the dates you choose, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_airbnb_scraper import AirbnbScraper

    scraper = AirbnbScraper()   # saved login (`airbnb-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # Airbnb stays for a city, region or neighbourhood
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["AirbnbScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class AirbnbScraper:
    """Airbnb Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="airbnb-scraper/0.1.0 (+https://github.com/quantumproxies/airbnb-scraper)", timeout=timeout)

    def search(
        self, location: str,
        *,
        checkin: Optional[str] = None,
        checkout: Optional[str] = None,
        adults: Optional[int] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Airbnb stay search for a place — title, type, nightly price, rating, reviews, beds and coordinates.

        Args:
            location: City, region or neighbourhood, e.g. "Rome", "Rome, Italy" or "Brooklyn, New York". Resolved by Airbnb's own search, exactly as typing it into the site would.
            checkin: Arrival date as YYYY-MM-DD. Must be given together with checkout; omit both to let Airbnb price each listing for its own suggested stay.
            checkout: Departure date as YYYY-MM-DD. Must be after checkin.
            adults: Number of adult guests (1–16). Omit for Airbnb's default of one.
            country: Country to run the search from, as an ISO 3166-1 alpha-2 code (us, gb, de...). Airbnb prices in that country's currency.
            max_results: How many stays to deliver at most (1–90). You pay only for delivered stays.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 90 rows, one per stay: see ``types.AirbnbStaysRow``.
        """
        payload = {
            "location": location,
            "checkin": checkin,
            "checkout": checkout,
            "adults": adults,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("airbnb_stays", payload, wait=wait, timeout=timeout)
