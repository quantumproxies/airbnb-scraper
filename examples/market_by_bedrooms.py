"""Nightly price of the Airbnb homes of an area, by number of bedrooms.

    python market_by_bedrooms.py "Lisbon, Portugal" --checkin 2026-12-01 --checkout 2026-12-03 --adults 2

Keeps homes only (hotel and bed-and-breakfast cards are left out), groups them
by bedrooms and writes listing count, lowest and median nightly price, median
rating and the share of Guest favorites: a pricing reference for hosts and
investors. Airbnb states a studio in words, so homes without a bedroom count
are grouped as "studio or not stated". Prices are for the dates you pass.
"""

import argparse
from collections import defaultdict
from statistics import median

from quanticdata_airbnb_scraper import AirbnbScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("location")
    parser.add_argument("--checkin", required=True, help="arrival date, YYYY-MM-DD")
    parser.add_argument("--checkout", required=True, help="departure date, YYYY-MM-DD")
    parser.add_argument("--adults", type=int, default=2)
    parser.add_argument("--max-results", type=int, default=90, help="stays to read (max 90)")
    parser.add_argument("--out", default="airbnb_by_bedrooms.csv")
    args = parser.parse_args()

    airbnb = AirbnbScraper()
    run = airbnb.search(args.location, checkin=args.checkin, checkout=args.checkout, adults=args.adults,
                        max_results=args.max_results)
    groups = defaultdict(list)
    for stay in run:
        if stay.get("is_hotel") or not stay.get("price_per_night"):
            continue
        groups[stay.get("bedrooms")].append(stay)

    summary = []
    for bedrooms in sorted(groups, key=lambda b: -1 if b is None else b):
        homes = groups[bedrooms]
        ratings = [h["rating"] for h in homes if h.get("rating")]
        summary.append({
            "bedrooms": "studio or not stated" if bedrooms is None else bedrooms,
            "homes": len(homes),
            "currency": next((h["currency"] for h in homes if h.get("currency")), ""),
            "lowest_per_night": min(h["price_per_night"] for h in homes),
            "median_per_night": round(median(h["price_per_night"] for h in homes), 2),
            "median_rating": round(median(ratings), 2) if ratings else "",
            "guest_favorite_share": round(sum(1 for h in homes if h.get("guest_favorite")) / len(homes), 2),
        })

    for s in summary:
        print(f"{str(s['bedrooms']):<22} {s['homes']:>3} homes  median {s['median_per_night']:>9,.2f} {s['currency']}"
              f"  rating {s['median_rating']}")
    write(summary, args.out)
    print(f"{len(summary)} groups written to {args.out}")


if __name__ == "__main__":
    main()
