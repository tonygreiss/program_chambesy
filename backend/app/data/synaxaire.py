from dataclasses import dataclass
import csv
from pathlib import Path

@dataclass
class SynaxaireEntry:
    day: int
    month: int
    saints: list[str]
    events: list[str]
    
def load_synaxaire_from_csv(file_path: str) -> dict:
    """Load synaxaire data from CSV file into a dictionary."""
    synaxaire_data = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            month_num = int(row['month_number'])
            day_num = int(row['day_number'])
            event = row['synaxaire']
            category = row['synaxaire_category']
            
            # Create key tuple of (month, day)
            key = (month_num, day_num)
            
            # Initialize entry if it doesn't exist
            if key not in synaxaire_data:
                synaxaire_data[key] = SynaxaireEntry(
                    day=day_num,
                    month=month_num,
                    saints=[],
                    events=[]
                )
            
            # Add event to appropriate list based on category
            if category in ['Martyre', 'Départ', 'Décès']:
                synaxaire_data[key].saints.append(event)
            else:
                synaxaire_data[key].events.append(event)
                
    return synaxaire_data

# Load data from CSV file
SYNAXAIRE_DATA = load_synaxaire_from_csv(Path(__file__).parent / 'synaxaire.csv') 