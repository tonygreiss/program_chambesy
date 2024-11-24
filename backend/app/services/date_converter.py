from convertdate import coptic, gregorian
from datetime import datetime, date
from app.services.synaxaire_service import SynaxaireService

class DateConverter:
    def __init__(self):
        self.synaxaire_service = SynaxaireService()

    def get_month_dates_with_synaxaire(self, year: int, month: int) -> list:
        """
        Get all dates in a month that have Synaxaire entries
        
        Parameters:
        -----------
        year : int
            Gregorian year
        month : int
            Gregorian month (1-12)
            
        Returns:
        --------
        list
            List of dictionaries containing dates and their Synaxaire entries
        """
        dates_with_entries = []
        
        # Get the number of days in the month
        if month == 2:
            days_in_month = 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28
        elif month in [4, 6, 9, 11]:
            days_in_month = 30
        else:
            days_in_month = 31
            
        # Check each day of the month
        for day in range(1, days_in_month + 1):
            # Convert to Coptic date
            coptic_date = coptic.from_gregorian(year, month, day)
            coptic_month, coptic_day = coptic_date[1], coptic_date[2]
            
            # Get Synaxaire entries for this date
            entries = self.synaxaire_service.get_entries_for_date(coptic_month, coptic_day)
            
            if entries:
                formatted_entries = self.synaxaire_service.format_entries(entries)
                
                # Create event strings for each category
                events = []
                if formatted_entries["martyrs"]:
                    events.append("Martyrs: " + "; ".join(formatted_entries["martyrs"]))
                if formatted_entries["saints"]:
                    events.append("Saints: " + "; ".join(formatted_entries["saints"]))
                if formatted_entries["commemorations"]:
                    events.append("Commémorations: " + "; ".join(formatted_entries["commemorations"]))
                if formatted_entries["other"]:
                    events.append("Autres: " + "; ".join(formatted_entries["other"]))
                
                dates_with_entries.append({
                    'date': f"{day}/{month}/{year}",
                    'event': "\n".join(events)
                })
        
        return dates_with_entries