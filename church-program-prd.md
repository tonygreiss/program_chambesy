# Church Program Generator - Product Requirements Document

## Overview
The Church Program Generator is a web application that automates the creation of monthly church programs by converting Gregorian dates to Coptic dates, matching saints/events from the Synaxaire, and generating a formatted document with schedules for multiple locations.

## Problem Statement
Currently, the process of creating monthly church programs is manual and time-consuming, involving:
- Manual date conversions between Gregorian and Coptic calendars
- Looking up saints and events in the Synaxaire
- Formatting weekly schedules
- Creating separate tables for different locations
- Maintaining consistent document formatting

## Solution
A web-based application that automates this process, allowing users to:
1. Select month and year
2. Input verses in French and Arabic
3. Generate a formatted document automatically

## Key Features

### Backend Features
1. **Date Conversion System**
   - Convert Gregorian to Coptic dates
   - Generate Coptic date codes
   - Handle calendar mapping logic

2. **Synaxaire Integration**
   - Match Coptic dates with saints/events
   - Support multiple events per date
   - Maintain data consistency

3. **Schedule Management**
   - Apply weekly recurring events
   - Handle special location schedules
   - Calculate monthly variations

4. **Document Generation**
   - Create formatted Word documents
   - Include logos and contact information
   - Generate formatted tables
   - Support multilingual content (French/Arabic)
   - Include QR code generation

### Frontend Features
1. **User Interface**
   - Month/year selector
   - Verse input fields (French/Arabic)
   - Generate button
   - Preview capability
   - Download functionality

## Technical Architecture

### Frontend Stack
- **Framework**: Next.js with TypeScript
- **UI Components**: Tailwind CSS with shadcn/ui
- **State Management**: React Hooks
- **HTTP Client**: Axios
- **Form Handling**: React Hook Form

### Backend Stack
- **Language**: Python 3.9+
- **Web Framework**: Flask with Flask-CORS
- **Date Conversion**: convertdate library
- **Document Generation**: python-docx
- **Data Storage**: CSV files
- **QR Code Generation**: qrcode library

### Development Tools
- **Version Control**: Git
- **Package Management**: 
  - Frontend: npm/yarn
  - Backend: pip
- **Deployment**: Docker
- **API Documentation**: Swagger/OpenAPI

## Data Structure

### Input Data
1. **Calendar Data**
   - Gregorian dates
   - Coptic dates
   - Date mappings

2. **Church Information**
   - Weekly schedules
   - Location details
   - Contact information

3. **Content**
   - Synaxaire entries
   - Monthly verses
   - Special events

### Output Format
- **File Type**: DOCX
- **Sections**:
  - Header with logos
  - Title section
  - Monthly verses
  - Geneva program table
  - Yverdon program table
  - Delemont program table
  - QR code section
  - Footer

## API Endpoints

### Backend API
```
POST /api/generate-program
    Request:
        - month: int
        - year: int
        - french_verse: string
        - arabic_verse: string
    Response:
        - document: binary (DOCX file)

GET /api/preview-program
    Request:
        - month: int
        - year: int
        - french_verse: string
        - arabic_verse: string
    Response:
        - html_preview: string
```

## Development Phases

### Phase 1: Core Backend Development
- Date conversion system
- Synaxaire integration
- Basic document generation
- API setup

### Phase 2: Frontend Development
- User interface implementation
- Form validation
- API integration
- Preview functionality

### Phase 3: Document Generation Enhancement
- Template refinement
- Formatting improvements
- QR code integration
- Multi-location support

### Phase 4: Testing and Deployment
- Unit testing
- Integration testing
- Docker configuration
- Deployment setup

## Future Enhancements
1. Program template customization
2. Multiple language support
3. Event management interface
4. Calendar synchronization
5. Email distribution system
6. Mobile responsiveness
7. User authentication
8. Backup and restore functionality

## Dependencies

### External Libraries
```python
# Backend
flask==2.0.1
flask-cors==3.0.10
convertdate==2.3.2
python-docx==0.8.11
qrcode==7.3.1
pandas==1.3.3

# Frontend
next==12.0.0
react==17.0.2
typescript==4.4.3
tailwindcss==2.2.19
axios==0.24.0
```

## Performance Requirements
- Document generation: < 5 seconds
- Page load time: < 2 seconds
- API response time: < 1 second
- Support for concurrent users: 50+

## Security Considerations
1. Input validation
2. CORS configuration
3. Rate limiting
4. Error handling
5. Data backup
6. Secure file handling

## Maintenance
- Regular backups of data files
- Monthly updates of calendar data
- Version control for templates
- Log monitoring
- Performance optimization

## Success Metrics
1. Reduction in program generation time
2. Error reduction in date mappings
3. User satisfaction
4. System reliability
5. Document accuracy

## Implementation Notes
1. Ensure proper handling of special cases in the Coptic calendar
2. Maintain formatting consistency across different word processors
3. Implement robust error handling for date conversions
4. Support for various document formats
5. Consider time zone handling for different locations
