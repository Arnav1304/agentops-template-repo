# BBQ Nation Chatbot

A conversational AI chatbot for BBQ Nation restaurant chain, handling table bookings, menu queries, and location information.

# Prototype


https://github.com/user-attachments/assets/14ee19ad-328f-4f10-9036-7260b5298c00




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
## State Machine Diagram

![deepseek_mermaid_20250518_689e58](https://github.com/user-attachments/assets/39d4869b-68ef-4d37-bcfc-2351dfe678b2)

## User Flow
![deepseek_mermaid_20250518_45e83c](https://github.com/user-attachments/assets/24077fd3-2ec9-4009-862c-01ed748e4b74)
 

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


