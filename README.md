# Student Management System - Microservices

## Project Overview
A backend Student Management System built using FastAPI microservices. The project separates authentication, student management, and course management into independent services connected through an API Gateway.

## Technologies Used
- Python
- FastAPI
- SQLite
- SQLAlchemy
- JWT Authentication
- HTTPX
- Postman
- Uvicorn

## Project Structure
- `api-gateway/` - Routes client requests to backend services
- `auth-service/` - User registration, login, and JWT authentication
- `student-service/` - Student CRUD operations
- `course-service/` - Course CRUD operations
- `postman/collection.json` - API testing collection

## Services and Ports
| Service | Port | Swagger Documentation |
|---|---:|---|
| API Gateway | 8000 | http://127.0.0.1:8000/docs |
| Auth Service | 8001 | http://127.0.0.1:8001/docs |
| Student Service | 8002 | http://127.0.0.1:8002/docs |
| Course Service | 8003 | http://127.0.0.1:8003/docs |

## Features
- User registration and login
- JWT-based authentication
- Token verification for protected API requests
- Create, read, update, and delete students
- Create, read, update, and delete courses
- API Gateway for routing requests
- SQLite databases for service data
- Postman collection for API testing

## How to Run

Activate the virtual environment from the project root:

```bash
source venv/bin/activate
```

Run each service in a separate terminal.

**Terminal 1 - Auth Service**
```bash
cd ~/Downloads/student-management
source venv/bin/activate
export JWT_SECRET_KEY="your-consistent-secret-key"
cd auth-service
uvicorn app.main:app --reload --port 8001
```

**Terminal 2 - Student Service**
```bash
cd ~/Downloads/student-management
source venv/bin/activate
cd student-service
uvicorn app.main:app --reload --port 8002
```

**Terminal 3 - Course Service**
```bash
cd ~/Downloads/student-management
source venv/bin/activate
cd course-service
uvicorn app.main:app --reload --port 8003
```

**Terminal 4 - API Gateway**
```bash
cd ~/Downloads/student-management
source venv/bin/activate
cd api-gateway
uvicorn main:app --reload --port 8000
```

Keep the same JWT secret for the Auth Service while it is running. If you restart it with a different secret, log in again to obtain a new token.

## API Testing
1. Open the API Gateway Swagger page at `http://127.0.0.1:8000/docs`.
2. Register a test account using `POST /auth/register`, or log in using an existing account.
3. Obtain an access token using `POST /auth/login`.
4. Authorize protected requests with the access token.
5. Test student and course CRUD operations through Swagger or import `postman/collection.json` into Postman.

## Notes
- This is a backend-only project; no frontend is included.
- Use test credentials only. Do not commit real passwords, tokens, or secret keys.
- Authentication and service routes should be tested with the required authorization token.