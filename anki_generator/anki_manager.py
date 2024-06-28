import json
import os

from dotenv import load_dotenv
from pyinputplus import inputInt


class AnkiManager:
    def __init__(self) -> None:
        load_dotenv()
        self.current_directory = os.getcwd()
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("PASSWORD")

    def load_json(self, json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        return data

    def get_files_in_directory(self, directory):
        """Gibt eine Liste der Dateien in einem Verzeichnis zurück."""
        try:
            files = [
                f
                for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))
            ]
            return files
        except FileNotFoundError:
            print(f"Directory {directory} not found.")
            return []

    def choose_file(self, files):
        """Ermöglicht dem Benutzer, eine Datei aus der Liste auszuwählen."""
        print("Choose a file:")
        for i, file in enumerate(files, start=1):
            print(f"{i}: {file}")
        choice = inputInt("Enter the number of the file", min=1, max=len(files))
        return files[choice - 1]
