from convertdate import coptic, gregorian
from datetime import datetime, date
from app.services.synaxaire_service import SynaxaireService

class DateConverter:
    @staticmethod
    def gregorian_to_coptic(gregorian_date: date) -> tuple:
        """
        Convert Gregorian date to Coptic date
        Returns: tuple (year, month, day)
        """
        return coptic.from_gregorian(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
    
    @staticmethod
    def get_month_dates(year: int, month: int) -> list:
        """
        Get all dates for a given month with their Coptic equivalents
        """
        start_date = date(year, month, 1)
        if month == 12:
            end_year = year + 1
            end_month = 1
        else:
            end_year = year
            end_month = month + 1
            
        end_date = date(end_year, end_month, 1)
        
        dates = []
        current_date = start_date
        while current_date < end_date:
            coptic_date = DateConverter.gregorian_to_coptic(current_date)
            dates.append({
                'gregorian': current_date,
                'coptic': coptic_date
            })
            current_date = date.fromordinal(current_date.toordinal() + 1)
            
        return dates 
    
    @staticmethod
    def get_month_dates_with_synaxaire(year: int, month: int) -> list:
        """Get all dates for a given month with their Coptic equivalents and Synaxaire entries"""
        dates = DateConverter.get_month_dates(year, month)
        synaxaire_service = SynaxaireService()
        
        for date_entry in dates:
            coptic_date = date_entry['coptic']
            synaxaire_entry = synaxaire_service.get_entries_for_date(
                coptic_date[1],  # month
                coptic_date[2]   # day
            )
            date_entry['synaxaire'] = synaxaire_service.format_entry(synaxaire_entry)
            
        return dates