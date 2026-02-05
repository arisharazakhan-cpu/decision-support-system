import csv
import json
from dateutil import parser as dtparser
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.product import Product
from app.models.data_source import DataSource
from app.models.raw_event import RawEvent

CSV_PATH = "../data/samples/events_demo.csv"


def get_or_create_product(db: Session, name: str) -> Product:
    existing = db.query(Product).filter(Product.name == name).one_or_none()
    if existing:
        return existing

    product = Product(name=name)
    db.add(product)
    db.flush()
    return product


def get_or_create_source(db: Session, name: str) -> DataSource:
    existing = db.query(DataSource).filter(DataSource.name == name).one_or_none()
    if existing:
        return existing

    source = DataSource(name=name, source_type="csv", refresh_minutes=None)
    db.add(source)
    db.flush()
    return source


def main():
    db = SessionLocal()
    try:
        inserted = 0

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                product = get_or_create_product(db, row["product_name"])
                source = get_or_create_source(db, row["source_name"])

                event_time = dtparser.isoparse(row["event_time"])
                payload = json.loads(row["payload_json"])

                event = RawEvent(
                    product_id=product.id,
                    source_id=source.id,
                    event_time=event_time,
                    payload=payload,
                )

                db.add(event)
                inserted += 1

        db.commit()
        print(f"Inserted {inserted} raw events")

    finally:
        db.close()


if __name__ == "__main__":
    main()
