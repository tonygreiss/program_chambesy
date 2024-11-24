from flask import Blueprint, request, jsonify, send_file
from app.services.date_converter import DateConverter
from app.services.synaxaire_service import SynaxaireService
from app.services.document_generator import DocumentGenerator
from flask_cors import cross_origin
import io
import logging

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
        # Log that we received a request
        print("Received request to generate program")
        
        # Get and log the request data
        data = request.get_json()
        print("Received data:", data)
        
        # Validate required fields
        required_fields = ['month', 'year', 'french_verse', 'arabic_verse']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Convert the data
        try:
            month = int(data['month'])
            year = int(data['year'])
        except ValueError as e:
            raise ValueError(f"Invalid month or year format: {str(e)}")
            
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be between 1 and 12, got {month}")
            
        # Get dates with synaxaire entries
        try:
            date_converter = DateConverter()
            dates_with_entries = date_converter.get_month_dates_with_synaxaire(year, month)
        except Exception as e:
            raise Exception(f"Error getting synaxaire entries: {str(e)}")
        
        # Generate the document
        try:
            doc_generator = DocumentGenerator()
            doc_bytes = doc_generator.generate(
                year=year,
                month=month,
                dates=dates_with_entries,
                french_verse=data['french_verse'],
                arabic_verse=data['arabic_verse']
            )
        except Exception as e:
            raise Exception(f"Error generating document: {str(e)}")
        
        # Return the document as a downloadable file
        return send_file(
            io.BytesIO(doc_bytes),
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'program_{month}_{year}.docx'
        )
        
    except Exception as e:
        print("Error occurred:", str(e))
        import traceback
        traceback.print_exc()  # This will print the full stack trace
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
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