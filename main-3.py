import sqlite3
import random
import string


class SeatManager:
    #this class is associated with memory management of the booking system, initializing
    #the seats and some other related functions

    def __init__(self):
        self.seats = self.initialize_seats()

    def initialize_seats(self):
        # initializing a dictionary for seats
        return {
            'A': ['F'] * 80,
            'B': ['F'] * 80,
            'C': ['F'] * 80,
            'D': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
            'E': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
            'F': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
        }

    # this function returns the index of a selected seat in seats
    def parse_seat(self, seat_input):
        seat_input = seat_input.strip().upper()
        if len(seat_input) < 2:
            return None, None, "Invalid seat format. Use '3A'."

        row = seat_input[-1]
        if row not in ['A', 'B', 'C', 'D', 'E', 'F']:
            return None, None, "Invalid row. Choose A-F."

        col_str = seat_input[:-1]
        if not col_str.isdigit():
            return None, None, "Column must be a number."

        col = int(col_str)
        if col < 1 or col > 80:
            return None, None, "Column must be 1-80."

        return row, col - 1, None

    # a modification to the initial program, some airline services provide an additional feature to the user
    # by given them an option of selecting an aisle or window seat, this function does the same functionality,
    # according to the sitting plan A and F and window seats and C and D are aisle seats, this function takes two
    # arguments one preference:String, entered by user and other seats, based upon preference this function returns
    # list of seats available
    def get_preferred_seats(self, preference):
        preferred_rows = []
        if preference == 'window':
            preferred_rows = ['A', 'F']  # Window seats in rows A/F
        elif preference == 'aisle':
            preferred_rows = ['C', 'D']  # Aisle seats in rows C/D

        preferred_seats = []
        for row in preferred_rows:
            for col in range(80):
                if self.seats[row][col] == 'F':
                    preferred_seats.append(f"{col + 1}{row}")
            preferred_seats.append("\n")
        return preferred_seats


    def display_status(self):
        #this function displays the complete status of each seat
        print("\n=== Seat Status ===")
        for row_label in ['A', 'B', 'C', 'D', 'E', 'F']:
            print(f"\nRow {row_label}:")
            for i in range(0, 80, 10):
                chunk = self.seats[row_label][i:i + 10]
                # Truncate booking references for display
                display_chunk = [s[:3] if s not in ['F', 'S'] else s for s in chunk]
                print(f"{i + 1:02}-{i + 10:02}: {' '.join(display_chunk)}")


class DatabaseHandler:
    #this class is responsible for the management of database

    def __init__(self):
        self.conn = sqlite3.connect('bookings.db')
        self.initialize_database()

    def initialize_database(self):
       # creating a table
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS bookings
                               (ref TEXT PRIMARY KEY,
                                passport TEXT NOT NULL,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                seat TEXT NOT NULL)''')

    def generate_booking_ref(self):
       #this function generates the booking ID, it crates an 8 digit reference number by random selecting letters and digits (0 to 9)
       #then it checks whether the generated ID already exits in database, if it exits it keeps on generating new IDs until one that is unique
       #from previous is created
        existing_refs = [row[0] for row in self.conn.execute("SELECT ref FROM bookings")]
        while True:
            ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if ref not in existing_refs:
                return ref

    def add_booking(self, ref, passport, first_name, last_name, seat):
       #add booking data to database
        with self.conn:
            self.conn.execute('''INSERT INTO bookings 
                              VALUES (?, ?, ?, ?, ?)''',
                              (ref, passport, first_name, last_name, seat))

    def delete_booking(self, ref):
        #deletes data from db
        with self.conn:
            self.conn.execute("DELETE FROM bookings WHERE ref=?", (ref,))

    def close(self):
        self.conn.close()


class BookingSystem:
    #this class run the application

    def __init__(self):
        self.seat_manager = SeatManager()
        self.db_handler = DatabaseHandler()

    def show_menu(self):
        print("\n===== Apache Airlines Seat Booking =====")
        print("1. Check Seat Availability")
        print("2. Book a Seat")
        print("3. Free a Seat")
        print("4. Show Booking Status")
        print("5. Exit")

    def handle_availability_check(self):
        #this function checks if the selected seat is available or not
        seat_input = input("Enter seat (e.g., 3A): ")
        row, col, error = self.seat_manager.parse_seat(seat_input)
        if error:
            print(error)
            return

        status = self.seat_manager.seats[row][col]
        if status == 'S':
            print(f"Seat {seat_input} is a storage area.") #selected seat can't be a storage area
        elif status == 'F':
            print(f"Seat {seat_input} is available.")
        else:
            print(f"Seat {seat_input} is booked (Ref: {status[:8]})")

    def handle_booking(self):
        #this function is for booking function
        preference = input("Choose preference (window/aisle/none): ").lower().strip()
        if preference in ['window', 'aisle']: #asking user's preference
            preferred = self.seat_manager.get_preferred_seats(preference)
            if preferred:
                print(f"Suggested {preference} seats (first 5): {', '.join(preferred[:5])}")

        seat_input = input("Enter seat to book: ").strip().upper()
        row, col, error = self.seat_manager.parse_seat(seat_input)
        if error:
            print(error)
            return

        if self.seat_manager.seats[row][col] != 'F':  #seat should not already be booked
            print(f"Seat {seat_input} is not available.")
            return

        # Getting passenger details
        passport = input("Passport number: ").strip()
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()

        # Generate and store booking
        ref = self.db_handler.generate_booking_ref()
        self.seat_manager.seats[row][col] = ref
        self.db_handler.add_booking(ref, passport, first_name, last_name, seat_input)
        print(f"Booked! Reference: {ref}")

    def handle_free_seat(self):
        # Free a seat
        seat_input = input("Enter seat to free: ").strip().upper()
        row, col, error = self.seat_manager.parse_seat(seat_input)
        if error:
            print(error)
            return

        current_ref = self.seat_manager.seats[row][col]
        if current_ref == 'F':
            print("Seat is already free")
            return

        self.db_handler.delete_booking(current_ref)
        self.seat_manager.seats[row][col] = 'F'
        print(f"Seat {seat_input} freed. Reference {current_ref} removed")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter choice (1-5): ")

            if choice == '1':
                self.handle_availability_check()
            elif choice == '2':
                self.handle_booking()
            elif choice == '3':
                self.handle_free_seat()
            elif choice == '4':
                self.seat_manager.display_status()
            elif choice == '5':
                self.db_handler.close()
                print("Exiting program. Thank you!")
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    app = BookingSystem()
    app.run()