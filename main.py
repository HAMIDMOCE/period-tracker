from datetime import datetime, timedelta
from pathlib import Path
import json


class PeriodTracker:

    def __init__(self):
        self.period_dates = []

    def add_period_date(self, date):
        if not date:
            return False, "Date cannot be empty."

        if date in self.period_dates:
            return False, "This date has already been recorded."

        if self.period_dates and date <= self.period_dates[-1]:
            return False, "Date must be after the last recorded period."

        self.period_dates.append(date)
        return True, "Date added successfully."

    def calculate_cycles(self):
        if len(self.period_dates) < 2:
            return []

        cycles = []
        for i in range(len(self.period_dates) - 1):
            cycles.append((self.period_dates[i+1] - self.period_dates[i]).days)

        return cycles

    def calculate_average_cycle(self):
        cycles = self.calculate_cycles()

        if not cycles:
            return None

        average = sum(cycles) / len(cycles)
        return average

    def predict_next_period(self):
        average = self.calculate_average_cycle()
        if average is None:
            return None

        last_period_date = self.period_dates[-1]

        predict_date = last_period_date + timedelta(days=round(average))
        return predict_date

    def calculate_remaining_days(self):
        predict_date = self.predict_next_period()

        if predict_date is None:
            return None

        today = datetime.today().date()

        remaining_days = (predict_date - today).days
        return remaining_days

    def to_dict(self):
        return {'period_dates' : [date.isoformat() for date in self.period_dates]}

    def delete_period_date(self, index):
        if not self.period_dates:
            return False, "No dates to delete."

        if index < 1 or index > len(self.period_dates):
            return False, "Invalid index."

        removed_date = self.period_dates.pop(index-1)
        return True, f"{removed_date} deleted successfully."

    def edit_period_date(self, index, new_date):
        if not self.period_dates:
            return False, "No dates to edit."

        if new_date in self.period_dates:
            return False, "This date has already been recorded."

        if index < 1 or index > len(self.period_dates):
            return False, "Invalid index."

        prev_date = self.period_dates[index-2] if index > 1 else None
        next_date = self.period_dates[index] if index < len(self.period_dates) else None

        if prev_date and new_date <= prev_date:
            return False, "New date must be after previous date."

        if next_date and new_date >= next_date:
            return False, "New date must be before next date."

        self.period_dates[index-1] = new_date
        return True, "date edited successfully."

    def save_data(self):
        dates = self.to_dict()

        with open('period_data.json', 'w') as file:
            json.dump(dates, file, indent=4)

    def load_data(self):
        file_path = Path('period_data.json')

        if not file_path.exists():
            self.period_dates = []
            return

        with open(file_path, 'r') as file:
            data = json.load(file)

        self.period_dates = [datetime.strptime(period_date, '%Y-%m-%d').date() for period_date in data['period_dates']]

    def __str__(self):
        if not self.period_dates:
            return "No period dates recorded."

        result = ""
        for n, date in enumerate(self.period_dates, start=1):
            if date == self.period_dates[-1]:
                result += f"{n}. period date: {date} (Last period date)"

            else:
                result += f"{n}. period date: {date}\n"

        return result

def display_menu():
    print("\n===== Period Tracker =====")
    print("1. Add period date")
    print("2. View period dates")
    print("3. Show cycle statistics")
    print("4. Predict next period")
    print("5. Delete period date")
    print("6. Edit period date")
    print("7. Save and Exit")

def receive_date(prompt):
    while True:
        user_date = input(prompt).strip()

        try:
            return datetime.strptime(user_date, "%Y-%m-%d").date()

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def main():
    tracker = PeriodTracker()
    tracker.load_data()

    while True:
        display_menu()

        choice = input('Choose an option: ').strip()

        if choice == '1':
            print('===== Add Period Date =====')
            while True:
                new_date = receive_date('Enter period date (YYYY-MM-DD): ')
                status, message = tracker.add_period_date(new_date)

                if status:
                    print(message)
                    break

                print(message)

        elif choice == '2':
            print('===== View Period Dates =====')
            print(tracker)

        elif choice == '3':
            print('===== Show Cycle Statistics =====')
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
            print('===== Predict Next Period =====')
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
            print("===== Delete Period Date =====")
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
            print('Good bye.')
            break

        else:
            print('Invalid choice.')

if __name__ == "__main__":
    main()