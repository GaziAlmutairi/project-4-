#initializing a dictionary for seats
def initialize_seats():
    seats = {
        'A': ['F'] * 80,
        'B': ['F'] * 80,
        'C': ['F'] * 80,
        'D': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
        'E': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
        'F': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
    }
    return seats

#this function returns the index of a selected seat in seats
def parse_seat(seat_input):
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

#a modification to the initial program, some airline services provide an additional feature to the user
#by given them an option of selecting an aisle or window seat, this function does the same functionality,
#according to the sitting plan A and F and window seats and C and D are aisle seats, this function takes two
#arguments one preference:String, entered by user and other seats, based upon preference this function returns
#list of seats available
def get_preferred_seats(preference, seats):
    preferred_rows = []
    if preference == 'window':
        preferred_rows = ['A', 'F']  # Window seats in rows A/F
    elif preference == 'aisle':
        preferred_rows = ['C', 'D']  # Aisle seats in rows C/D

    preferred_seats = []
    for row in preferred_rows:
        for col in range(80):
            if seats[row][col] == 'F':
                preferred_seats.append(f"{col + 1}{row}")
        preferred_seats.append("\n")
    return preferred_seats

#the main algorithm of the program
def main():
    seats = initialize_seats()

    while True:
        print("\n===== Apache Airlines Seat Booking =====")
        print("1. Check Seat Availability")
        print("2. Book a Seat")
        print("3. Free a Seat")
        print("4. Show Booking Status")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        #Displaying Available Seats
        if choice == '1':
            seat_input = input("Enter seat (e.g., 3A): ")
            row, col, error = parse_seat(seat_input)
            if error:
                print(error)
                continue

            status = seats[row][col]
            if status == 'X':
                print(f"Seat {seat_input} is an aisle (X). Cannot book.")
            elif status == 'S':
                print(f"Seat {seat_input} is a storage area (S). Cannot book.")
            elif status == 'R':
                print(f"Seat {seat_input} is already booked.")
            else:
                print(f"Seat {seat_input} is available (F).")

        #Booking of Seat
        elif choice == '2':
            preference = input("Choose seat preference (window/aisle/none): ").lower().strip()
            if preference == "window":
                preferred_seats = get_preferred_seats(preference, seats)
                for seat in preferred_seats:
                    print(seat,end=" ")
                print()
            elif preference == "aisle":
                preferred_seats = get_preferred_seats(preference, seats)
                for seat in preferred_seats:
                    print(seat, end=" ")
                print()

            seat_input = input("Enter seat to book: ").strip().upper()
            row, col, error = parse_seat(seat_input)
            if error:
                print(error)
                continue
            if seats[row][col] == 'F':
                seats[row][col] = 'R'
                print(f"Seat {seat_input} booked successfully!")
            else:
                status = seats[row][col]
                if status == 'R':
                    print(f"Seat {seat_input} is already booked.") #seat should not already be booked
                elif status == 'S':
                    print(f"Seat {seat_input} is a storage area.") #selected seat can't be a storage area
                else:
                    print(f"Seat {seat_input} cannot be booked.") #seat can't be in aisle area or any other invalidity

        # Freeing a seat
        elif choice == '3':
            seat_input = input("Enter seat to free (e.g., 3A): ")
            row, col, error = parse_seat(seat_input)
            if error:
                print(error)
                continue

            if seats[row][col] == 'R':
                seats[row][col] = 'F'
                print(f"Seat {seat_input} freed successfully!")
            else:
                print(f"Seat {seat_input} is not booked.")

        # Displaying the sitting plan 
        elif choice == '4':
            print("\n=== Full Seat Status (F=Free, R=Booked, X=Aisle, S=Storage) ===")
            for row in ['A', 'B', 'C', 'D', 'E', 'F']:
                print(f"\nRow {row}:")
                for i in range(0, 80, 10):
                    start = i + 1
                    end = i + 10
                    seats_slice = ''.join(seats[row][i:i + 10])
                    print(f"Seats {start:02}-{end:02}: {seats_slice}")

        # Exit
        elif choice == '5':
            print("Exiting program. Thank you!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()