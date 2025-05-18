# BBQ Nation Chatbot

A conversational AI chatbot for BBQ Nation restaurant chain, handling table bookings, menu queries, and location information.

## Features

- **Table Booking System**
  - Contact collection with validation
  - Location selection (Bangalore/Delhi)
  - Slot management (Lunch/Dinner)
  - Special date handling
  - Booking confirmation and cancellation

- **Menu System**
  - Dietary preference handling (Veg/Non-veg/Jain)
  - Category-wise menu display
  - Item details and descriptions

- **Location Management**
  - City and area selection
  - Location-specific information
  - Nearest location suggestions

## Project Structure

```
bbq-nation-chatbot/
├── src/
│   ├── core/           # Core business logic
│   ├── data/           # JSON data files
│   ├── api/            # Flask API endpoints
│   ├── state_machine/  # Conversation states
│   └── utils/          # Helper functions
├── tests/              # Unit and integration tests
├── assets/             # Prompts and diagrams
└── scripts/            # Utility scripts
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Arnav1304/agentops-template-repo.git
cd bbq-nation-chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python src/api/app.py
```

## API Endpoints

- **Chat API**: `/api/chat`
  - Method: POST
  - Purpose: Main conversation endpoint for Retell AI

- **Menu API**: `/api/menu`
  - Method: GET
  - Purpose: Menu queries and dietary preferences

- **Location API**: `/api/locations`
  - Method: GET
  - Purpose: Location information and availability

- **Booking API**: `/api/booking`
  - Methods: POST, GET, DELETE
  - Purpose: Table booking management

## Testing

Run unit tests:
```bash
pytest tests/unit
```

Run integration tests:
```bash
pytest tests/integration
```

## Development

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update documentation
4. Use meaningful commit messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support or queries, please contact:
- Email: support@bbqnation.com
- Phone: 1800-XXX-XXXX 