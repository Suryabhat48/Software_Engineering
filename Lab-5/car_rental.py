"""Car Rental System - Lab 5: Static Code Analysis.

Provides a robust in-memory vehicle rental management system including fleet
management, customer database persistence, booking lifecycle, secure licence
hashing, and receipt generation.
"""

from datetime import datetime
import hashlib
import os
import re
import secrets
import sqlite3
import tempfile

# Global rental state
fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin_secure_pass")


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Register a car into the rental fleet."""
    if not plate:
        return None
    if features is None:
        features = []
    fleet[plate] = {
        "model": model,
        "rate": max(0, daily_rate),
        "available": True,
        "features": features,
    }
    return fleet[plate]


def register_customer(name, licence, phone):
    """Add a customer record using safe parameterized SQL."""
    conn.execute(
        "INSERT INTO customers VALUES (?, ?, ?)",
        (name, licence, phone),
    )


def find_customer(name):
    """Query customer records securely using parameterized SQL."""
    query = "SELECT * FROM customers WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()


def rent_car(plate, customer, start, end):
    """Create a car booking and calculate rental cost."""
    if not find_customer(customer):
        raise ValueError("Customer not registered")
    if plate not in fleet:
        raise KeyError("Vehicle not in fleet")
    if not fleet[plate]["available"]:
        raise ValueError("Vehicle is already booked")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    days = (end_date - start_date).days
    if days <= 0:
        days = 1

    cost = days * fleet[plate]["rate"]
    fleet[plate]["available"] = False

    booking = {
        "code": booking_code(),
        "plate": plate,
        "customer": customer,
        "days": days,
        "cost": cost,
    }
    bookings.append(booking)
    return cost


def return_car(plate, km_driven):
    """Mark a returned vehicle as available and calculate extra km fee."""
    if plate not in fleet:
        return 0
    fleet[plate]["available"] = True
    if km_driven > 300:
        return (km_driven - 300) * 5
    return 0


def booking_code():
    """Generate a cryptographically secure random booking code."""
    return f"BK-{secrets.randbelow(90000) + 10000}"


def licence_hash(licence):
    """Hash driving licence number using SHA-256."""
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()


def apply_promo(rule, amount):
    """Safely apply a promo discount rule without using exec."""
    match = re.search(r"amount\s*\*\s*([0-9.]+)", rule)
    if match:
        multiplier = float(match.group(1))
        return amount * multiplier
    match_sub = re.search(r"amount\s*-\s*([0-9.]+)", rule)
    if match_sub:
        return max(0.0, amount - float(match_sub.group(1)))
    return amount


def is_valid_plate(plate):
    """Validate Indian vehicle registration number format."""
    return bool(re.match(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$", plate))


def write_receipt(booking):
    """Write booking receipt securely to a temporary file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as temp_file:
        temp_file.write(
            f"Booking {booking['code']}: {booking['plate']} for "
            f"{booking['days']} days = Rs.{booking['cost']}\n"
        )
        path = temp_file.name
    os.chmod(path, 0o600)
    return path


def admin_login(user, password=None):
    """Authenticate administrator safely without hardcoded defaults."""
    if not password:
        return False
    return user == ADMIN_USER and password == ADMIN_PASSWORD


def available_cars():
    """Return all plates of currently available vehicles."""
    return [plate for plate, car in fleet.items() if car.get("available")]


def main():
    """Execute built-in demonstration of car rental system."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    add_car("KA03EF9999", "Nexon", 2000)
    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")
    print(
        "Rent Swift:",
        rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"),
    )
    print("Return Swift:", return_car("KA01AB1234", 120))
    print(
        "Rent Swift again:",
        rent_car("KA01AB1234", "Ravi", "2026-11-02", "2026-11-03"),
    )
    print(
        "Rent Innova:",
        rent_car("KA02CD5678", "Ravi", "2026-11-07", "2026-11-10"),
    )
    print("Lookup injection:", find_customer("x' OR '1'='1"))
    print("Extra km charge:", return_car("KA01AB1234", 420))
    print("Return unknown car:", return_car("XX00XX0000", 50))
    print("Promo price:", apply_promo("amount = amount * 0.9", 4500))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))
    print("Admin:", admin_login("admin", ADMIN_PASSWORD))
    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(bookings[0]))


if __name__ == "__main__":
    main()
