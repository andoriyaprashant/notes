# Notes App Backend API
 
A backend application for a multi-user notes service built using FastAPI and PostgreSQL.
 
This project provides secure REST APIs for:
- User registration and authentication
- Notes CRUD operations
- Note sharing between users
- Note version history
- Search functionality
- Pagination
- Dockerized deployment
---
 
# Tech Stack
 
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Docker
- Pydantic
- Passlib (bcrypt)
---
 
# Features
 
## Authentication
- User Registration
- User Login
- JWT-based authentication
## Notes
- Create notes
- Read notes
- Update notes
- Delete notes
## Sharing
- Share notes with other registered users
- Shared users can access shared notes
## Custom Feature
### Note Version History
Whenever a note is updated, the previous version is stored in the `note_history` table.
 
This feature was added to:
- improve user experience,
- allow tracking note changes,
- simulate real-world note applications like Google Docs or Notion revision history.
## Stretch Goals Implemented
- Pagination for `/notes`
- Search endpoint `/search?q=keyword`
- Dockerized application
---
 
# Project Structure
 
```text
notes-app/
│
├── app/
│   ├── routes/
│   ├── utils/
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```
 
# Environment Variables
Create a `.env` file in the project root:
 
```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
 
# Local Setup
 
## 1. Clone Repository
 
```
git clone https://github.com/andoriyaprashant/notes.git
cd notes
```
 
## 2. Create Virtual Environment
 
### Windows
 
```
python -m venv venv
venv\Scripts\activate
```
 
### Linux / WSL
 
```
python3 -m venv venv
source venv/bin/activate
```
 
## 3. Install Dependencies
 
```
pip install -r requirements.txt
```
 
## 4. Configure PostgreSQL
 
Create a PostgreSQL database named:
 
```
notesdb
```
 
Update `.env` with your PostgreSQL connection string.
Example:
 
```
DATABASE_URL=postgresql://postgres:password@localhost/notesdb
```
 
## 5. Run Application
 
```
python run.py
```
 
Server runs at:
 
```
http://localhost:8000
```
 
Swagger docs:
 
```
http://localhost:8000/docs
```
 
OpenAPI schema:
 
```
http://localhost:8000/openapi.json
```
 
# Docker Setup
 
## Build Docker Image
 
```
docker build -t notes-app .
```
 
## Run Docker Container
 
```
docker run -p 10000:10000 notes-app
```
 
# Deployment
 
This project is deployed on Render.
Base URL:
 
```
https://notes-jdwu.onrender.com
```
 
API documentation:
 
```
https://notes-jdwu.onrender.com/docs
```
 
OpenAPI schema:
 
```
https://notes-jdwu.onrender.com/openapi.json
```
 
# API Endpoints
 
## Authentication
 
### Register User
 
```
POST /register
```
 
Payload:
 
```
{
  "email": "user@example.com",
  "password": "password123"
}
```
 
### Login
 
```
POST /login
```
 
Payload:
 
```
{
  "email": "user@example.com",
  "password": "password123"
}
```
 
Response:
 
```
{
  "access_token": "jwt_token"
}
```
 
## Notes APIs
 
### Get All Notes
 
```
GET /notes
```
 
Supports:
 
*  pagination 
*  shared notes visibility 
Headers:
 
```
Authorization: Bearer <jwt_token>
```
 
### Get Single Note
 
```
GET /notes/{id}
```
 
### Create Note
 
```
POST /notes
```
 
Payload:
 
```
{
  "title": "My Note",
  "content": "Note content"
}
```
 
### Update Note
 
```
PUT /notes/{id}
```
 
### Delete Note
 
```
DELETE /notes/{id}
```
 
## Share API
 
### Share Note
 
```
POST /notes/{id}/share
```
 
Payload:
 
```
{
  "share_with_email": "friend@example.com"
}
```
 
## Search API
 
### Search Notes
 
```
GET /search?q=keyword
```
 
## History API
 
### Get Note History
 
```
GET /notes/{id}/history
```
 
Returns previous versions of the note.
 
# Security Features
 
*  Password hashing using bcrypt 
*  JWT authentication 
*  Authorization checks for note ownership 
*  Shared note access validation 
*  Input validation using Pydantic 
# Edge Cases Handled
 
*  Duplicate email registration 
*  Invalid login credentials 
*  Empty note title/content 
*  Unauthorized note access 
*  Sharing note with self 
*  Duplicate note sharing 
*  Invalid note/user access 

# Author
 
Prashant Andoriya
Email: prashantandoriya@gmail.com
 