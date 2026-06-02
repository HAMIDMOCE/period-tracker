from datetime import datetime


class PeriodTracker:

    def __init__(self):
        self.period_dates = []

    def add_period_date(self, date):
        if not date:
            return False, "Date cannot be empty."

        if date  in self.period_dates:
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


def receive_date(prompt):
    while True:
        user_date = input(prompt).strip()

        try:
            return datetime.strptime(user_date, "%Y-%m-%d").date()

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def main():
    tracker = PeriodTracker()

    first_period_date = receive_date("Enter last period date (YYYY-MM-DD): ")
    tracker.add_period_date(first_period_date)

    try:
        number_of_user_dates = int(input('How many additional period dates do you want to add? ').strip())

        for index in range(number_of_user_dates):
            while True:
                new_date = receive_date('Enter period date (YYYY-MM-DD): ')
                status, message = tracker.add_period_date(new_date)

                if status:
                    print(message)
                    break

                print(message)

    except ValueError:
        print('Invalid input.')

    print("\n===== Period Tracker =====")
    print(tracker)

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


if __name__ == "__main__":
    main()