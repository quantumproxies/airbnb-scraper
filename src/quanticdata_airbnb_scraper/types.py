"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class AirbnbStaysRow(TypedDict, total=False):
    """One row of `airbnb-scraper search` (airbnb_stays v1.1.2)."""

    rank: int
    """Position in Airbnb's order for this response. Airbnb re-ranks between requests, so this is not a stable property of the listing."""
    listing_id: Optional[str]
    """Airbnb listing id — the number in the /rooms/ URL."""
    title: Optional[str]
    """Card heading as Airbnb writes it, property type then area ("Apartment in Monti")."""
    property_type: Optional[str]
    """Property type taken from the head of the title ("Apartment", "Condo", "Penthouse"). Null when the title is not of that shape."""
    name: Optional[str]
    """The host's own listing name."""
    subtitle: Optional[str]
    """Card subtitle — usually the listing name, sometimes a short description."""
    rating: Optional[float]
    """Average rating out of 5. Null on a listing with no reviews yet."""
    reviews: Optional[int]
    """Number of reviews."""
    guest_favorite: bool
    """True when Airbnb badges the listing a Guest favorite."""
    badges: Optional[List[str]]
    """Badge labels shown on the card, e.g. ["Guest favorite"], ["Superhost"] or ["Luxe"]. Airbnb's flexible-date chip shares the same list and is excluded — it is a date range, not a badge, and check_in/check_out already carry it."""
    price_per_night: Optional[float]
    """Nightly rate as Airbnb states it in its own price breakdown ("5 nights x $741.37"), never total ÷ nights. When a stay discount is listed as its own line, this is the rate before that discount."""
    price_total: Optional[float]
    """Price shown on the card for the whole stay, after any discount."""
    price_original_total: Optional[float]
    """Struck-through stay total on a discounted card; null when the card is not discounted."""
    price_text: Optional[str]
    """The price exactly as printed on the card, e.g. "$3,707"."""
    price_qualifier: Optional[str]
    """What the price covers, in Airbnb's words: "for 5 nights" or "night"."""
    nights: Optional[int]
    """Nights the priced stay covers."""
    currency: Optional[str]
    """ISO currency of the prices, from the symbol Airbnb printed. Airbnb prices in the currency of the country the search runs from (--country); a bare "$" is reported as USD only for us and left null elsewhere rather than guessed."""
    free_cancellation: bool
    """True when the card carries Airbnb's free-cancellation highlight."""
    beds: Optional[int]
    """Beds, from the card's bed line ("3 beds", "4 double beds") — not the bedroom count."""
    bedrooms: Optional[int]
    """Bedrooms. Null on a studio, which Airbnb states in words."""
    bathrooms: Optional[float]
    """Baths, halves included (1.5). Null when Airbnb states it in words ("Half-bath")."""
    bed_info: Optional[str]
    """The card's bed and bath line verbatim, e.g. "3 bedrooms, 3 beds, 2 baths"."""
    check_in: Optional[str]
    """Check-in the price covers (YYYY-MM-DD): the date you asked for, or the one Airbnb chose for this listing when you asked for none."""
    check_out: Optional[str]
    """Check-out the price covers (YYYY-MM-DD)."""
    latitude: Optional[float]
    """Airbnb's approximate map point — it publishes a fuzzed location until a booking is confirmed, not the exact address."""
    longitude: Optional[float]
    """Approximate longitude, as above."""
    image: Optional[str]
    """First photo on the card."""
    photo_count: int
    """Photos in the card's carousel — not the listing's full gallery."""
    url: Optional[str]
    """Listing URL, composed from the listing id."""
    photos: List[str]
    """Up to six photo URLs from the card carousel."""
    superhost: bool
    """True when the host is a Superhost."""
    is_hotel: bool
    """True when the card is a hotel or bed-and-breakfast listed as a property with several rooms."""
    property_id: Optional[str]
    """Airbnb property id on hotel and bed-and-breakfast cards."""
    rooms_available: Optional[int]
    """Rooms available for the dates, on hotel and bed-and-breakfast cards."""
    pay_later: bool
    """True when the card offers to reserve with nothing to pay upfront."""
