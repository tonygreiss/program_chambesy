from flask import Blueprint, request, jsonify
from app.services.date_converter import DateConverter
from app.services.synaxaire_service import SynaxaireService
from app.services.document_generator import DocumentGenerator

main = Blueprint('main', __name__)

@main.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!'
    })

@main.route('/api/generate-program', methods=['POST'])
def generate_program():
    data = request.get_json()
    
    try:
        month = int(data.get('month'))
        year = int(data.get('year'))
        french_verse = data.get('french_verse')
        arabic_verse = data.get('arabic_verse')
        
        # Get dates with Synaxaire entries
        dates = DateConverter.get_month_dates_with_synaxaire(year, month)
        
        # Generate document
        doc_generator = DocumentGenerator()
        doc_bytes = doc_generator.generate(
            year=year,
            month=month,
            dates=dates,
            french_verse=french_verse,
            arabic_verse=arabic_verse
        )
        
        # Return document
        doc_buffer = BytesIO(doc_bytes)
        doc_buffer.seek(0)
        
        return send_file(
            doc_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'program_{year}_{month}.docx'
        )
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Add new endpoint to fetch Synaxaire entries
@main.route('/api/synaxaire/<int:month>/<int:day>', methods=['GET'])
def get_synaxaire(month: int, day: int):
    try:
        synaxaire_service = SynaxaireService()
        entry = synaxaire_service.get_entries_for_date(month, day)
        
        return jsonify({
            'status': 'success',
            'data': synaxaire_service.format_entry(entry)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400