# 404 - Emission Reduction App
## Description
404 is a mobile application developed to motivate both companies and citizens to reduce their greenhouse gas emissions. The app provides tools and tracking features to help users make a positive impact on the environment.

## Prerequisites
- GitHub Desktop
- Docker
- Docker Compose

## Installation
1. Clone the Repository
- Download GitHub desktop from https://desktop.github.com/download/
- Open GitHub Desktop
- Click on "File" > "Clone Repository"
- Select the "404" repository
- Choose the location where you want to save the project
- Click "Clone"

2. Install Docker and Docker Compose
- Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Run the installer and follow the instructions
- Docker Compose is included with Docker Desktop
- Run the Backend
- Navigate to the project folder in your terminal

3. Run the project (Backend API)
- From VisualStudio, Cursor or Terminal run the following command from the folder 404/Backend:


```
docker-compose up
```

## Structure
The Backend folder contains the following structure

backend/

├── app/

│   ├── api/            # Endpoints

│   ├── core/           # General application settings

│   ├── models/         # Data models

│   ├── schemas/        # Classes used for input and outputs

│   └── services/       # Logic

├── tests/              # Unit and integration tests

├── Dockerfile          # Docker configuration

└── docker-compose.yml  # Service configuration


### Folder Descriptions
- api/: Defines API routes (endpoints)
- core/: General application settings and functions like database connections, middleware, security issues
- models/: Defines schemas and data models for the postgresql database
- schemas/: Contains all the data classes for unputs and outputs of the API endpoints
- services/: Handles all the logic behind the endpoints (direct communication to database, transform data, etc)
