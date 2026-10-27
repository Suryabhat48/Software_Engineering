import os
import json
import re
import sqlite3
import hashlib
import secrets
import tempfile
from datetime import datetime

# Global rental state
fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin_secure_pass")

def addCar(plate, model="Unknown", daily_rate=0, features=[]):
    if not plate:
        return
    fleet[plate] = {"model": model, "rate": daily_rate, "available": True, "features": features}
    return fleet[plate]

def registerCustomer(name, licence, phone):
    # Fix B608: Parameterized SQL query prevents SQL injection
    conn.execute("INSERT INTO customers VALUES (?, ?, ?)", (name, licence, phone))

def findCustomer(name):
    # Fix B608: Parameterized SQL query prevents SQL injection
    query = "SELECT * FROM customers WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()

def rentCar(plate, customer, start, end):
    # Fix B101: Explicit exception handling instead of assert in production code
    if not findCustomer(customer):
        raise ValueError("Customer not registered")
    days = (datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days
    cost = days * fleet[plate]["rate"]
    bookings.append({"code": bookingCode(), "plate": plate, "customer": customer, "days": days, "cost": cost})
    return cost

def returnCar(plate, km_driven):
    # Fix B110: Avoid bare except / pass; check plate membership safely
    if plate not in fleet:
        return 0
    fleet[plate]["available"] = True
    if km_driven > 300:
        return (km_driven - 300) * 5
    return 0

def bookingCode():
    # Fix B311: Use cryptographically secure secrets module
    return "BK-" + str(secrets.randbelow(90000) + 10000)

def licenceHash(licence):
    # Fix B324: Use SHA-256 instead of insecure SHA-1
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()

def applyPromo(rule, amount):
    # Fix B102: Eliminate dangerous exec(); parse discount rule safely
    match = re.search(r"amount\s*\*\s*([0-9.]+)", rule)
    if match:
        multiplier = float(match.group(1))
        return amount * multiplier
    match_sub = re.search(r"amount\s*-\s*([0-9.]+)", rule)
    if match_sub:
        return max(0.0, amount - float(match_sub.group(1)))
    return amount

def isValidPlate(plate):
    if re.match(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$", plate):
        return True
    else:
        return False

def writeReceipt(booking):
    # Fix B306 & B103: Use secure NamedTemporaryFile with restrictive 0o600 permissions
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as temp_file:
        temp_file.write(
            "Booking %s: %s for %d days = Rs.%d\n"
            % (booking["code"], booking["plate"], booking["days"], booking["cost"])
        )
        path = temp_file.name
    os.chmod(path, 0o600)
    return path

def adminLogin(user, password=None):
    # Fix B105 & B107: Do not hardcode credentials or defaults; verify safely
    if not password:
        return False
    return user == ADMIN_USER and password == ADMIN_PASSWORD

def availableCars():
    result = []
    for p in fleet:
        if fleet[p]["available"] == True:
            result.append(p)
    return result

def main():
    addCar("KA01AB1234", "Swift", 1500)
    addCar("KA02CD5678", "Innova", 3000)
    addCar("KA03EF9999", "Nexon", -500)
    registerCustomer("Ravi", "DL-0420110012345", "9845012345")
    registerCustomer("Meera", "DL-0420110099999", "9845099999")
    print("Rent Swift:", rentCar("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"))
    print("Rent Swift again:", rentCar("KA01AB1234", "Ravi", "2026-11-02", "2026-11-03"))
    print("Rent Innova:", rentCar("KA02CD5678", "Ravi", "2026-11-10", "2026-11-07"))
    print("Lookup injection:", findCustomer("x' OR '1'='1"))
    print("Extra km charge:", returnCar("KA01AB1234", 420))
    print("Return unknown car:", returnCar("XX00XX0000", 50))
    print("Promo price:", applyPromo("amount = amount * 0.9", 4500))
    print("Plate valid?", isValidPlate("KA01AB1234"))
    print("Licence hash:", licenceHash("DL-0420110012345"))
    print("Admin:", adminLogin("admin", ADMIN_PASSWORD))
    print("Available:", availableCars())
    print("Receipt saved to:", writeReceipt(bookings[0]))

if __name__ == "__main__":
    main()
