from typing import Optional, List, Dict
from app.data.synaxaire import SYNAXAIRE_DATA, SynaxaireEntry
import os

from dataclasses import dataclass
from typing import Optional, List, Dict
import csv
import os

@dataclass
class SynaxaireEntry:
    month_number: int
    day_number: int
    month_name: str
    description: str
    category: str
    is_martyre: bool

class SynaxaireService:
    def __init__(self):
        """Initialize the service and load data"""
        self._data = self._load_synaxaire_data()

    def _load_synaxaire_data(self) -> Dict[tuple, List[SynaxaireEntry]]:
        """Load Synaxaire data from CSV file"""
        data = {}
        csv_path = os.path.join(os.path.dirname(__file__), '../data/synaxaire_v2.csv')
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) >= 6:  # Ensure row has all required fields
                        month = int(row[0])
                        day = int(row[1])
                        entry = SynaxaireEntry(
                            month_number=month,
                            day_number=day,
                            month_name=row[2],
                            description=row[3],
                            category=row[4],
                            is_martyre=(row[5] == '1')
                        )
                        
                        key = (month, day)
                        if key not in data:
                            data[key] = []
                        data[key].append(entry)
                        
        except Exception as e:
            print(f"Error loading Synaxaire data: {e}")
            return {}
            
        return data

    def get_entries_for_date(self, month: int, day: int) -> List[SynaxaireEntry]:
        """Get all Synaxaire entries for a specific Coptic date"""
        return self._data.get((month, day), [])

    def format_entries(self, entries: List[SynaxaireEntry]) -> Dict[str, List[str]]:
        """Format Synaxaire entries by category"""
        formatted = {
            "martyrs": [],
            "saints": [],
            "commemorations": [],
            "other": []
        }
        
        for entry in entries:
            description = entry.description
            if entry.is_martyre:
                formatted["martyrs"].append(description)
            elif entry.category == "Commémoration":
                formatted["commemorations"].append(description)
            elif entry.category in ["Décès", "Départ"]:
                formatted["saints"].append(description)
            else:
                formatted["other"].append(description)
                
        return formatted