from pathlib import Path
import json

class JSONStorage:

    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def load(self):
        file_path = Path(self.filename)

        if not file_path.exists():
            return {'period_dates': []}

        try:
            with open(self.filename, 'r') as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return {'period_dates': []}