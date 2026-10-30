"""Airbnb stays in several destinations for the same dates, in one CSV.

    python compare_cities.py "Lisbon, Portugal" "Porto, Portugal" "Seville, Spain" --checkin 2026-12-01 --checkout 2026-12-03

Every row keeps the destination it came from. For each destination it prints
how many stays came back, the median nightly price and the median rating.
Prices are for the dates and guests you pass.
"""

import argparse
from statistics import median

from quanticdata_airbnb_scraper import AirbnbScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("locations", nargs="+", help='places as you would type them on Airbnb, e.g. "Rome, Italy"')
    parser.add_argument("--checkin", required=True, help="arrival date, YYYY-MM-DD")
    parser.add_argument("--checkout", required=True, help="departure date, YYYY-MM-DD")
    parser.add_argument("--adults", type=int, default=2)
    parser.add_argument("--max-results", type=int, default=90, help="stays per destination (max 90)")
    parser.add_argument("--out", default="airbnb_destinations.csv")
    args = parser.parse_args()

    airbnb = AirbnbScraper()
    rows = []
    for location in args.locations:
        run = airbnb.search(location, checkin=args.checkin, checkout=args.checkout, adults=args.adults,
                            max_results=args.max_results)
        nightly = [s["price_per_night"] for s in run if s.get("price_per_night")]
        ratings = [s["rating"] for s in run if s.get("rating")]
        currency = next((s["currency"] for s in run if s.get("currency")), "")
        line = f"{location}: {len(run)} stays"
        if nightly:
            line += f", median {median(nightly):,.2f} {currency} a night"
        if ratings:
            line += f", median rating {median(ratings):.2f}"
        print(line)
        rows.extend({"destination": location, **s} for s in run)

    write(rows, args.out)
    print(f"{len(rows)} stays written to {args.out}")


if __name__ == "__main__":
    main()
