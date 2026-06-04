from datetime import datetime, timedelta

class PeriodTracker:

    def __init__(self, storage):
        self.storage = storage
        self.period_dates = []

    def load_data(self):
        data = self.storage.load()

        self.period_dates = [datetime.strptime(d, '%Y-%m-%d').date() for d in data.get('period_dates', [])]

    def save_data(self):
        data = {'period_dates' : [d.isoformat() for d in self.period_dates]}
        self.storage.save(data)

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

        i = index - 1

        prev_date = self.period_dates[i-1] if i > 0 else None
        next_date = self.period_dates[i+1] if i < len(self.period_dates) - 1 else None

        if prev_date and next_date:
            if not (prev_date < new_date < next_date):
                return False, "New date must be between previous and next date."

        elif prev_date and not next_date:
            if new_date <= prev_date:
                return False, "New date must be after previous date."

        elif not prev_date and next_date:
            if new_date >= next_date:
                return False, "New date must be before next date."

        self.period_dates[i] = new_date
        return True, "Date edited successfully."

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