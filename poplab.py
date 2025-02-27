from pyflightdata import FlightData
from datetime import datetime
import getpass

email = input("Enter Flightradar24 email: ")
password = getpass.getpass("Enter Flightradar24 password: ")

f = FlightData()
f.login(email, password)

user_input = input("Enter tail numbers (seperated by commas) or press Enter for N350XX and N621MM: ").strip()

if user_input:
    tail_numbers = [t.strip().upper() for t in user_input.split(",")]
else:
    tail_numbers = ["N350XX", "N621MM"]

def last_flight(tail_number):
    try:
        history = f.get_history_by_tail_number(tail_number, page=1, limit=1)
        if not history:
            print(f"No flight history found for {tail_number}.")
            return
        
        last_flight = history[0]
        departure = last_flight.get('departure', {})
        arrival = last_flight.get('arrival', {})

        print(f"\nLatest flight for {tail_number}:")
        print(f"From: {departure.get('airport', {}).get('name', 'N/A')} ({departure.get('airport', {}).get('code', 'N/A')})")
        print(f"To: {arrival.get('airport', {}).get('name', 'N/A')} ({arrival.get('airport', {}).get('code', 'N/A')})")

    except Exception as e:
        print(f"Error fetching data for {tail_number}: {e}")

for tail_number in tail_numbers:
    last_flight(tail_number)
