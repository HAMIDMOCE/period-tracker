from datetime import datetime
from storage import JSONStorage
from tracker import PeriodTracker

def receive_date(prompt):
    while True:
        user_date = input(prompt).strip()

        try:
            return datetime.strptime(user_date, "%Y-%m-%d").date()

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def display_menu():
    print("\n===== Period Tracker =====")
    print("1. Add period date")
    print("2. View period dates")
    print("3. Show cycle statistics")
    print("4. Predict next period")
    print("5. Delete period date")
    print("6. Edit period date")
    print("7. Save and Exit")

def main():
    storage = JSONStorage('period_data.json')
    tracker = PeriodTracker(storage)

    tracker.load_data()

    while True:
        display_menu()

        choice = input('Choose an option: ').strip()

        if choice == '1':
            print('\n===== Add Period Date =====')
            new_date = receive_date('Enter period date (YYYY-MM-DD): ')
            status, message = tracker.add_period_date(new_date)

            print(message)

        elif choice == '2':
            print('\n===== View Period Dates =====')
            print(tracker)

        elif choice == '3':
            print('\n===== Show Cycle Statistics =====')
            cycles = tracker.calculate_cycles()
            if cycles:
                for n, cycle in enumerate(cycles, start=1):
                    print(f"Cycle {n}: {cycle} days")

            else:
                print('Not enough data to calculate cycle lengths.')

            average = tracker.calculate_average_cycle()
            if average is not None:
                print(f"Average cycle length: {average:.1f} days")

            else:
                print('Not enough data to calculate average cycle.')

        elif choice == '4':
            print('\n===== Predict Next Period =====')
            predict_date = tracker.predict_next_period()
            if predict_date is not None:
                print(f"Next period is expected on: {predict_date}")

            else:
                print('Not enough data to predict the next period date.')

            remaining_days = tracker.calculate_remaining_days()
            if remaining_days is not None:
                if remaining_days > 0:
                    print(f"Days remaining until next period: {remaining_days}")

                elif remaining_days == 0:
                    print('Your period starts today.')

                else:
                    print(f"The predicted period date was {abs(remaining_days)} days ago.")

            else:
                print("Not enough data to calculate remaining days.")

        elif choice == '5':
            print("\n===== Delete Period Date =====")
            print(tracker)

            try:
                index = int(input('Enter number to delete: ').strip())
                status, message = tracker.delete_period_date(index)

                print(message)

            except ValueError:
                print('Invalid input.')

        elif choice == '6':
            print(tracker)
            try:
                index = int(input('Enter number to edit: ').strip())
                new_date = receive_date('Enter new period date (YYYY-MM-DD): ')

                status, message = tracker.edit_period_date(index, new_date)

                print(message)

            except ValueError:
                print('Invalid input.')

        elif choice == '7':
            tracker.save_data()
            print('Saved, Good bye.')
            break

        else:
            print('Invalid choice.')

if __name__ == "__main__":
    main()