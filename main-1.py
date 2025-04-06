
def initialize_seats():
    seats = {
        'A': ['F'] * 80,
        'B': ['F'] * 80,
        'C': ['X'] * 80,
        'D': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
        'E': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
        'F': ['F'] * 76 + ['S', 'S'] + ['F'] * 2,
    }
    return seats


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

        elif choice == '2':
            seat_input = input("Enter seat to book (e.g., 3A): ")
            row, col, error = parse_seat(seat_input)
            if error:
                print(error)
                continue

            if seats[row][col] == 'F':
                seats[row][col] = 'R'
                print(f"Seat {seat_input} booked successfully!")
            else:
                print(f"Cannot book seat {seat_input}. It is invalid or already booked.")

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