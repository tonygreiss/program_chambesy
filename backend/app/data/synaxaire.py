class SynaxaireEntry:
    def __init__(self, day: int, month: int, saints: list, events: list):
        self.day = day
        self.month = month
        self.saints = saints
        self.events = events

# Sample data structure - In production, this would come from a database
SYNAXAIRE_DATA = {
    # Format: (month, day): SynaxaireEntry
    (1, 1): SynaxaireEntry(
        day=1,
        month=1,
        saints=["St. John the Short", "St. Rewis"],
        events=["Beginning of Coptic New Year (Nayrouz)"]
    ),
    # Add more entries...
} 