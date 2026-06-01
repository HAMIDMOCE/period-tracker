from datetime import datetime


class PeriodTracker:

    def __init__(self, last_period_date):
        self.last_period_date = last_period_date

    def __str__(self):
        return f"Last period date: {self.last_period_date}"


def receive_date(prompt):
    while True:
        user_date = input(prompt).strip()

        if not user_date:
            print("Date cannot be empty.")
            continue

        try:
            return datetime.strptime(user_date, "%Y-%m-%d").date()

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def main():
    last_period_date = receive_date("Enter last period date (YYYY-MM-DD): ")

    tracker = PeriodTracker(last_period_date)

    print("\n===== Period Tracker =====")
    print(tracker)


if __name__ == "__main__":
    main()