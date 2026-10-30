"""Airbnb nightly prices for one place across a run of check-in dates.

    python price_calendar.py "Lisbon, Portugal" --start 2026-12-01 --dates 6 --step 7 --nights 2

Prices the same stay length starting on --dates check-in dates, --step days
apart, and appends one summary row per date to airbnb_calendar.csv: stays
found, lowest and median nightly price, and the median for homes only (hotel
cards left out). Run it again later to see how the same dates are repriced.
"""

import argparse
import csv
import os
from datetime import date, datetime, timedelta, timezone
from statistics import median

from quanticdata_airbnb_scraper import AirbnbScraper

FIELDS = ["checked_at", "location", "check_in", "check_out", "nights", "stays", "currency",
          "lowest_per_night", "median_per_night", "median_per_night_homes"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("location")
    parser.add_argument("--start", required=True, help="first check-in date, YYYY-MM-DD")
    parser.add_argument("--dates", type=int, default=6, help="how many check-in dates to price")
    parser.add_argument("--step", type=int, default=7, help="days between check-in dates")
    parser.add_argument("--nights", type=int, default=2)
    parser.add_argument("--adults", type=int, default=2)
    parser.add_argument("--max-results", type=int, default=90, help="stays per date (max 90)")
    parser.add_argument("--out", default="airbnb_calendar.csv")
    args = parser.parse_args()

    airbnb = AirbnbScraper()
    start = date.fromisoformat(args.start)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        for i in range(args.dates):
            check_in = start + timedelta(days=i * args.step)
            check_out = check_in + timedelta(days=args.nights)
            run = airbnb.search(args.location, checkin=check_in.isoformat(), checkout=check_out.isoformat(),
                                adults=args.adults, max_results=args.max_results)
            nightly = [s["price_per_night"] for s in run if s.get("price_per_night")]
            homes = [s["price_per_night"] for s in run if s.get("price_per_night") and not s.get("is_hotel")]
            row = {
                "checked_at": checked_at,
                "location": args.location,
                "check_in": check_in.isoformat(),
                "check_out": check_out.isoformat(),
                "nights": args.nights,
                "stays": len(run),
                "currency": next((s["currency"] for s in run if s.get("currency")), ""),
                "lowest_per_night": min(nightly) if nightly else "",
                "median_per_night": round(median(nightly), 2) if nightly else "",
                "median_per_night_homes": round(median(homes), 2) if homes else "",
            }
            writer.writerow(row)
            print(f"{row['check_in']}: {row['stays']} stays, median {row['median_per_night']} {row['currency']} a night")
    print(f"{args.dates} dates appended to {args.out}")


if __name__ == "__main__":
    main()
