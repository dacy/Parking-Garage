# Parking Garage Management System

A FastAPI-based parking garage management system that uses AI to provide optimized parking recommendations.

## Features

- Real-time parking spot tracking
- AI-powered parking recommendations
- Building and garage management
- Multiple entrance support
- Zone and floor-based organization
- Historical parking data tracking

## API Endpoints

### Parking Recommendations

#### Get Parking Recommendation
```http
POST /api/v1/parking/recommendation
```

Request Body:
```json
{
    "user_working_location": "Building A",
    "user_preferred_entrance": "Hwy 121"
}
```

Response:
```json
{
    "user_preferred_entrance": "Hwy 121",
    "user_working_location": "Building A",
    "recommended_garage_and_floor": "Garage C, Floor 3",
    "availability_floor_percent": 85,
    "availability_garage_percent": 70
}
```

### Garage Information

#### Get All Garages
```http
GET /api/v1/garages
```

#### Get Garage by ID
```http
GET /api/v1/garages/{garage_id}
```

## Data Models

### Buildings
- Building A
- Building B
- Building C
- Building F

### Entrances
- Leadership Dr
- Hwy 121
- Headquarters Dr
- Communication Pkwy

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Schema

The system uses SQLite with the following main tables:
- garages
- floor
- zone
- spot
- buildings
- building_to_garage
- entrance
- entrance_to_garage
- spot_change

## AI Integration

The parking recommendation system uses AI to:
- Analyze current parking availability
- Consider user preferences
- Calculate optimal parking spots
- Provide real-time recommendations

## Development

The project structure follows FastAPI best practices:
```
.
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── parking.py
│       │   └── garage.py
│       └── schemas/
│           ├── parking.py
│           └── garage.py
├── models.py
├── main.py
└── requirements.txt
``` 