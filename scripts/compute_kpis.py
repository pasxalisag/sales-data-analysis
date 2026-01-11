#!/usr/bin/env python3
"""
Compute core sales KPIs from the raw sales dataset.

Input:
  data/raw_sales_data.csv

Output (printed to console):
  - Total Revenue
  - Total Units Sold
  - Total Invoices
  - Average Order Value (AOV)
  - Average Revenue per Pharmacy
  - Top Product Category (by revenue)
  - Top Region (by revenue)

Usage:
  python scripts/compute_kpis.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw_sales_data.csv"


def to_float(x: str) -> float:
    x = x.strip()
    if x == "":
        return 0.0
    return float(x)


def to_int(x: str) -> int:
    x = x.strip()
    if x == "":
        return 0
    return int(float(x))


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing dataset: {DATA_PATH}")

    total_revenue = 0.0
    total_units = 0
    invoices = set()

    revenue_by_category: dict[str, float] = defaultdict(float)
    revenue_by_region: dict[str, float] = defaultdict(float)
    revenue_by_pharmacy: dict[str, float] = defaultdict(float)

    with DATA_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {
            "invoice_id",
            "region",
            "product_category",
            "quantity",
            "revenue",
            "pharmacy_id",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Dataset is missing columns: {sorted(missing)}")

        for row in reader:
            invoice_id = row["invoice_id"].strip()
            region = row["region"].strip()
            category = row["product_category"].strip()
            pharmacy_id = row["pharmacy_id"].strip()

            qty = to_int(row["quantity"])
            rev = to_float(row["revenue"])

            invoices.add(invoice_id)
            total_units += qty
            total_revenue += rev

            revenue_by_category[category] += rev
            revenue_by_region[region] += rev
            revenue_by_pharmacy[pharmacy_id] += rev

    total_invoices = len(invoices)
    aov = (total_revenue / total_invoices) if total_invoices else 0.0
    avg_rev_per_pharmacy = (total_revenue / len(revenue_by_pharmacy)) if revenue_by_pharmacy else 0.0

    top_category = max(revenue_by_category.items(), key=lambda x: x[1])[0] if revenue_by_category else "N/A"
    top_region = max(revenue_by_region.items(), key=lambda x: x[1])[0] if revenue_by_region else "N/A"

    print("=== Sales KPIs (from raw_sales_data.csv) ===")
    print(f"Total Revenue: €{total_revenue:,.2f}")
    print(f"Total Units Sold: {total_units}")
    print(f"Total Invoices: {total_invoices}")
    print(f"Average Order Value (AOV): €{aov:,.2f}")
    print(f"Average Revenue per Pharmacy: €{avg_rev_per_pharmacy:,.2f}")
    print(f"Top Product Category (by revenue): {top_category}")
    print(f"Top Region (by revenue): {top_region}")


if __name__ == "__main__":
    main()
