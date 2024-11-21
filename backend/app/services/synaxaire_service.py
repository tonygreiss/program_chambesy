from typing import Optional, List, Dict
from app.data.synaxaire import SYNAXAIRE_DATA, SynaxaireEntry

class SynaxaireService:
    @staticmethod
    def get_entries_for_date(month: int, day: int) -> Optional[SynaxaireEntry]:
        """Get Synaxaire entries for a specific Coptic date"""
        return SYNAXAIRE_DATA.get((month, day))
    
    @staticmethod
    def get_entries_for_month(month: int) -> Dict[int, SynaxaireEntry]:
        """Get all Synaxaire entries for a specific Coptic month"""
        return {
            day: entry 
            for (m, day), entry in SYNAXAIRE_DATA.items() 
            if m == month
        }
    
    @staticmethod
    def format_entry(entry: SynaxaireEntry) -> dict:
        """Format a Synaxaire entry for API response"""
        if not entry:
            return None
            
        return {
            "saints": entry.saints,
            "events": entry.events
        } 