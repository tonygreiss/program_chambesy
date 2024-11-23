from typing import List, Dict
from pathlib import Path
import csv

class SynaxaireEntry:
    """Represents a single Synaxaire entry for a specific date"""
    def __init__(
        self,
        saints: List[str],
        events: List[str]
    ):
        self.saints = saints
        self.events = events

def load_synaxaire_from_csv(file_path: Path) -> Dict[tuple, SynaxaireEntry]:
    """Load synaxaire data from CSV file into a dictionary."""
    data = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            month = int(row['month'])
            day = int(row['day'])
            saints = [s.strip() for s in row['saints'].split(',')]
            events = [e.strip() for e in row['events'].split(',')]
            
            data[(month, day)] = SynaxaireEntry(saints=saints, events=events)
                
    return data

# Load data from CSV file
SYNAXAIRE_DATA = load_synaxaire_from_csv(Path(__file__).parent / 'synaxaire.csv') 