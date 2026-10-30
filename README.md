# Airbnb Scraper

[![ci](https://github.com/quantumproxies/airbnb-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/airbnb-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Airbnb from Python or the command line: the stays Airbnb lists for a city, region or neighbourhood, with nightly price, stay total, rating, review count, bedrooms, beds, baths, badges, photos and approximate map point, for the dates and guests you choose, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/airbnb-scraper
airbnb-scraper login
airbnb-scraper search "Lisbon, Portugal" --checkin 2026-12-01 --checkout 2026-12-03 --adults 2 --max-results 90 -o lisbon.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=airbnb-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `airbnb-scraper search` | city, region or neighbourhood, optional dates | Title, type, nightly price, rating, reviews, beds and coordinates, 35 fields per row ([fields and price](https://quanticdata.io/collectors/airbnb-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=airbnb-scraper)) | up to 90 |

Prices depend on the dates you pass: give `--checkin` and `--checkout` (YYYY-MM-DD) and `--adults` and every price is for that stay. Without dates Airbnb prices each listing for its own suggested stay, and `check_in` and `check_out` say which. `price_per_night` is the rate in Airbnb's own price breakdown, `price_total` the card total after any discount. `latitude` and `longitude` are Airbnb's approximate map point, not the exact address. Hotel and bed-and-breakfast cards are flagged with `is_hotel`.

## Sample output

A real row from `airbnb-scraper search "Lisbon, Portugal" --checkin 2026-12-01 --checkout 2026-12-03 --adults 2 --max-results 3` (2026-10-23):

```json
{
  "url": "https://www.airbnb.com/rooms/1195206575229724261",
  "beds": 2,
  "name": "Alfama Village with Air-conditioned door 11",
  "rank": 3,
  "image": "https://a0.muscache.com/im/pictures/miso/Hosting-1195206575229724261/original/50005e8b-d20e-4bd9-b6dc-4bad6361e684.jpeg",
  "title": "Apartment in Lisbon",
  "badges": [
    "Guest favorite"
  ],
  "nights": 2,
  "photos": [
    "https://a0.muscache.com/im/pictures/miso/Hosting-1195206575229724261/original/50005e8b-d20e-4bd9-b6dc-4bad6361e684.jpeg",
    "https://a0.muscache.com/im/pictures/hosting/Hosting-1195206575229724261/original/60efb7f6-c178-4fb6-8118-4d3a75042370.jpeg"
  ],
  "rating": 4.84,
  "reviews": 178,
  "bed_info": "2 bedrooms, 2 single beds, 1 bath",
  "bedrooms": 2,
  "check_in": "2026-12-01",
  "currency": "USD",
  "is_hotel": false,
  "subtitle": "Alfama duplex with Tram 28 outside",
  "bathrooms": 1,
  "check_out": "2026-12-03",
  "pay_later": false,
  "superhost": false,
  "listing_id": "1195206575229724261",
  "price_text": "$152",
  "photo_count": 6,
  "price_total": 152,
  "property_id": null,
  "property_type": "Apartment",
  "guest_favorite": true,
  "price_per_night": 75.74,
  "price_qualifier": "for 2 nights",
  "rooms_available": null,
  "free_cancellation": false,
  "price_original_total": null
}
```

## Python

```python
from quanticdata_airbnb_scraper import AirbnbScraper

airbnb = AirbnbScraper()  # saved login, or QUANTICDATA_API_KEY

stays = airbnb.search("Lisbon, Portugal", checkin="2026-12-01", checkout="2026-12-03", adults=2, max_results=90)
for s in stays:
    print(s["listing_id"], s["price_per_night"], s["currency"], s["rating"], s["reviews"], s["name"])
stays.to_csv("lisbon.csv")

homes = [s for s in stays if not s["is_hotel"]]
favorites = [s for s in homes if s["guest_favorite"]]
print(len(homes), "homes,", len(favorites), "of them Guest favorites")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Compare destinations**: Price the same dates in several cities and get one CSV with every stay, plus the median nightly price and rating of each destination. See [`examples/compare_cities.py`](examples/compare_cities.py).
- **Price calendar**: Price one place for the same stay length on a run of check-in dates and see how nightly rates move across weeks, holidays and low season. See [`examples/price_calendar.py`](examples/price_calendar.py).
- **Pricing reference for hosts**: Group the homes of an area by bedrooms and get listing count, median and lowest nightly price, median rating and the share of Guest favorites. See [`examples/market_by_bedrooms.py`](examples/market_by_bedrooms.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `airbnb-scraper run <id> -o out.csv` collects it later.

### `airbnb-scraper search`

Airbnb stay search for a place — title, type, nightly price, rating, reviews, beds and coordinates.

```
airbnb-scraper search LOCATION [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `LOCATION` | string |  | City, region or neighbourhood, e.g. "Rome", "Rome, Italy" or "Brooklyn, New York". Resolved by Airbnb's own search, exactly as typing it into the site would. |
| `--checkin` | string |  | Arrival date as YYYY-MM-DD. Must be given together with checkout; omit both to let Airbnb price each listing for its own suggested stay. |
| `--checkout` | string |  | Departure date as YYYY-MM-DD. Must be after checkin. |
| `--adults` | integer |  | Number of adult guests (1–16). Omit for Airbnb's default of one. |
| `--country` | string |  | Country to run the search from, as an ISO 3166-1 alpha-2 code (us, gb, de...). Airbnb prices in that country's currency. |
| `--max-results` | integer | `18` | How many stays to deliver at most (1–90). You pay only for delivered stays. |

## Output fields

<details><summary><code>airbnb-scraper search</code>: 35 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position in Airbnb's order for this response. Airbnb re-ranks between requests, so this is not a stable property of the listing. |
| `listing_id` | string or null | Airbnb listing id — the number in the /rooms/ URL. |
| `title` | string or null | Card heading as Airbnb writes it, property type then area ("Apartment in Monti"). |
| `property_type` | string or null | Property type taken from the head of the title ("Apartment", "Condo", "Penthouse"). Null when the title is not of that shape. |
| `name` | string or null | The host's own listing name. |
| `subtitle` | string or null | Card subtitle — usually the listing name, sometimes a short description. |
| `rating` | number or null | Average rating out of 5. Null on a listing with no reviews yet. |
| `reviews` | integer or null | Number of reviews. |
| `guest_favorite` | boolean | True when Airbnb badges the listing a Guest favorite. |
| `badges` | string[] or null | Badge labels shown on the card, e.g. ["Guest favorite"], ["Superhost"] or ["Luxe"]. Airbnb's flexible-date chip shares the same list and is excluded — it is a date range, not a badge, and check_in/check_out already carry it. |
| `price_per_night` | number or null | Nightly rate as Airbnb states it in its own price breakdown ("5 nights x $741.37"), never total ÷ nights. When a stay discount is listed as its own line, this is the rate before that discount. |
| `price_total` | number or null | Price shown on the card for the whole stay, after any discount. |
| `price_original_total` | number or null | Struck-through stay total on a discounted card; null when the card is not discounted. |
| `price_text` | string or null | The price exactly as printed on the card, e.g. "$3,707". |
| `price_qualifier` | string or null | What the price covers, in Airbnb's words: "for 5 nights" or "night". |
| `nights` | integer or null | Nights the priced stay covers. |
| `currency` | string or null | ISO currency of the prices, from the symbol Airbnb printed. Airbnb prices in the currency of the country the search runs from (--country); a bare "$" is reported as USD only for us and left null elsewhere rather than guessed. |
| `free_cancellation` | boolean | True when the card carries Airbnb's free-cancellation highlight. |
| `beds` | integer or null | Beds, from the card's bed line ("3 beds", "4 double beds") — not the bedroom count. |
| `bedrooms` | integer or null | Bedrooms. Null on a studio, which Airbnb states in words. |
| `bathrooms` | number or null | Baths, halves included (1.5). Null when Airbnb states it in words ("Half-bath"). |
| `bed_info` | string or null | The card's bed and bath line verbatim, e.g. "3 bedrooms, 3 beds, 2 baths". |
| `check_in` | string or null | Check-in the price covers (YYYY-MM-DD): the date you asked for, or the one Airbnb chose for this listing when you asked for none. |
| `check_out` | string or null | Check-out the price covers (YYYY-MM-DD). |
| `latitude` | number or null | Airbnb's approximate map point — it publishes a fuzzed location until a booking is confirmed, not the exact address. |
| `longitude` | number or null | Approximate longitude, as above. |
| `image` | string or null | First photo on the card. |
| `photo_count` | integer | Photos in the card's carousel — not the listing's full gallery. |
| `url` | string or null | Listing URL, composed from the listing id. |
| `photos` | string[] | Up to six photo URLs from the card carousel. |
| `superhost` | boolean | True when the host is a Superhost. |
| `is_hotel` | boolean | True when the card is a hotel or bed-and-breakfast listed as a property with several rooms. |
| `property_id` | string or null | Airbnb property id on hotel and bed-and-breakfast cards. |
| `rooms_available` | integer or null | Rooms available for the dates, on hotel and bed-and-breakfast cards. |
| `pay_later` | boolean | True when the card offers to reserve with nothing to pay upfront. |

</details>

## Sign-in and API keys

- `airbnb-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `airbnb-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `airbnb-scraper login --api-key`.
- `airbnb-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=airbnb-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/airbnb_stays/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"location": "Lisbon, Portugal", "checkin": "2026-12-01", "checkout": "2026-12-03", "adults": 2, "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=airbnb-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=airbnb-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Airbnb scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a place and, if you want, your dates and guests, and get rows back; the requests run on QuanticData's side. It reads Airbnb's public search results only and returns no host names or exact addresses; you are responsible for respecting Airbnb's terms and the data-protection rules that apply to how you use the data.

**Do the prices depend on the dates?**

Yes. With --checkin and --checkout every price is for that stay and that number of adults; without dates Airbnb prices each listing for its own suggested stay, given in check_in and check_out. Run the same place on other dates to compare.

**How many stays can one run return?**

Up to 90 stays per run; ask for fewer with --max-results and you pay only for what is delivered. Run neighbourhoods one by one to cover a large city.

**Can I export to CSV or Excel?**

Add -o stays.csv (or .json, .jsonl). Lists such as badges and photos are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/price_calendar.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Booking.com Scraper](https://github.com/quantumproxies/booking-scraper): Booking scraper for Python and the command line.
- [Google Hotels Scraper](https://github.com/quantumproxies/google-hotels-scraper): Google Hotels scraper for Python and the command line.
- [Google Flights Scraper](https://github.com/quantumproxies/google-flights-scraper): Google Flights scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=airbnb-scraper).
