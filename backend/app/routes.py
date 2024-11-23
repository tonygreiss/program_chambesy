from flask import Blueprint, request, jsonify, send_file
from app.services.date_converter import DateConverter
from app.services.synaxaire_service import SynaxaireService
from app.services.document_generator import DocumentGenerator
from flask_cors import cross_origin
import io

main = Blueprint('main', __name__)

@main.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!'
    })

@main.route('/api/generate-program', methods=['POST'])
@cross_origin()
def generate_program():
    try:
        # Get data from request
        data = request.get_json()
        
        # Log received data for debugging
        print("Received data:", data)
        
        # Extract values
        month = data.get('month')
        year = data.get('year')
        french_verse = data.get('french_verse')
        arabic_verse = data.get('arabic_verse')
        
        # Validate required fields
        if not all([month, year, french_verse, arabic_verse]):
            return jsonify({
                'error': 'Missing required fields'
            }), 400
            
        # Generate document
        doc_generator = DocumentGenerator()
        doc_bytes = doc_generator.generate(
            year=year,
            month=month,
            dates=[],  # You can add actual dates later
            french_verse=french_verse,
            arabic_verse=arabic_verse
        )
        
        # Create in-memory file
        doc_io = io.BytesIO(doc_bytes)
        doc_io.seek(0)
        
        # Return the file
        return send_file(
            doc_io,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'program_{year}_{month}.docx'
        )
        
    except Exception as e:
        print("Error:", str(e))  # Log the error
        return jsonify({
            'error': str(e)
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