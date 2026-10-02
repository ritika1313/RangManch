# RangManch
RangManch, a Pune based theatre booking startup, a reviews API audience can rate &amp; review plays. The API powers their app's review section &amp; average rating display.
🎭 Rangmanch Reviews API
A full CRUD REST API for theatre reviews, built with FastAPI +
SQLModel + SQLite.
The API allows users to:
- Create reviews
- Read/list reviews
- Update reviews
- Delete reviews
- Get average ratings for a play
- Filter reviews by play
- Paginate review results
🏗️ Solution Architecture
The project follows a simple API → model → database flow:
                         POST /reviews
                              │
                              ▼
                      ┌─────────────────┐
                      │  Create Review  │
                      └────────┬────────┘
                               │
                               ▼
┌────────────────┐       ┌───────────────┐
│  Client / App  │ ─────►│   FastAPI     │
└────────────────┘       │    Server     │
                         └───────┬───────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   GET /reviews          PATCH /reviews/{id}    DELETE /reviews/{id}
          │                      │                      │
          ▼                      ▼                      ▼
   List Reviews             Update Review          Delete Review
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 ▼
                         ┌───────────────┐
                         │  SQLModel     │
                         │    Models     │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ SQLite DB     │
                         │ rangmanch.db  │
                         └───────────────┘
Main Flow
Client → FastAPI → SQLModel → SQLite
FastAPI receives the HTTP request, validates the data, performs the
required database operation through a SQLModel Session, and returns
the response.
🎯 Interview Preparation
This section is my preparation checklist for explaining this project in
interviews/viva.
1. SQLModel for Database Models
Learning:
SQLModel is used for database models and combines SQLAlchemy +
Pydantic.

Interview points
- What is SQLModel?
- Why use SQLModel instead of writing raw SQL?
- What is the difference between a SQLModel table model and a normal
  SQLModel?
- What does table=True mean?
- What is a primary key?
- Why is id optional before inserting a record?
- What does Field(ge=1, le=5) do?
- Why is play_name indexed?
- What is the purpose of created_at?
- Why use timezone-aware datetime?
2. SQLite as a Zero-Configuration Database
Learning:
SQLite is used as a zero-configuration database for this project.

The database is stored locally as:
rangmanch.db
Interview points
- What is SQLite?
- Why is SQLite suitable for a small backend/project?
- What does sqlite:///rangmanch.db mean?
- Where is the database stored?
- What are the limitations of SQLite compared with PostgreSQL/MySQL?
- What happens when the application starts and the tables do not
  exist?
3. FastAPI Lifespan Events
Learning:
FastAPI lifespan events are used for startup/shutdown logic.

In this project, table creation happens during application startup.
Application starts
       ↓
lifespan()
       ↓
create_tables()
       ↓
yield
       ↓
Application runs
       ↓
Shutdown
Interview points
- What is a lifespan event in FastAPI?
- What happens before yield?
- What happens after yield?
- Why create database tables during startup?
- What is the difference between startup logic and request handling?
4. Session Dependency Injection
Learning:
FastAPI dependency injection is used to provide a database session to
API routes.

The project uses:
def get_session():
    with Session(engine) as session:
        yield session
Routes receive it using:
session: Session = Depends(get_session)
Interview points
- What is dependency injection?
- What does Depends() do?
- Why create a database session per request?
- Why use yield inside get_session()?
- When is the session closed?
- What is the difference between an engine and a session?
5. Full CRUD Operations
The API implements complete CRUD operations.
  Operation   HTTP Method   Endpoint                Purpose
  Create      POST          /review/              Create a review
  Read All    GET           /review/              Get reviews
  Read One    GET           /review/{review_id}   Get one review
  Update      PATCH         /review/{review_id}   Partially update a review
  Delete      DELETE        /review/{review_id}   Delete a review
Interview points
- Explain the complete CRUD flow.
- Why use POST for creating data?
- Why use GET for reading?
- Why use PATCH for partial updates?
- Difference between PUT and PATCH?
- Why use DELETE for removing a review?
- What status code should be returned when a review does not exist?
6. Pagination with skip / limit
The list endpoint supports pagination.
Example:
GET /review/?skip=0&limit=10
Meaning:
- skip=0 → start from the first review
- limit=10 → return at most 10 reviews
The API also validates the values:
skip: int = Query(0, ge=0)
limit: int = Query(10, ge=1, le=50)
Interview points
- What is pagination?
- Why is pagination important for APIs?
- What does skip mean?
- What does limit mean?
- Why put a maximum limit such as 50?
- What problems can occur if an API returns thousands of records at
  once?
7. Aggregation Queries --- Average Rating
The API provides an endpoint to calculate the average rating of a play.
GET /review/average/{play_name}
It uses database aggregation:
AVG(rating)
COUNT(id)
Example response:
{
  "play_name": "Hamlet",
  "average_rating": 4.25,
  "total_reviews": 20
}
Interview points
- What is an aggregation query?
- What does AVG() do?
- What does COUNT() do?
- Why calculate the average in the database?
- What happens when a play has no reviews?
- Why round the average rating?
- Why return the total number of reviews?
🔍 Project Architecture --- File Responsibilities
RangManch/
│
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── rangmanch.db
│
└── routes/
    ├── __init__.py
    └── reviews.py
main.py
Responsible for:
- Creating the FastAPI application
- Lifespan/startup handling
- Creating database tables
- Registering the review router
- Root endpoint
models.py
Contains:
Review
Database table model.
ReviewCreate
Input model used when creating a review.
ReviewRead
Response model used when returning a review.
ReviewUpdate
Input model used for partial updates.
This separation helps control what data the API accepts and returns.
database.py
Responsible for:
- Database URL
- SQLModel engine
- Table creation
- Database session dependency
routes/reviews.py
Contains the review API endpoints:
POST    /review/
GET     /review/
GET     /review/{review_id}
GET     /review/average/{play_name}
PATCH   /review/{review_id}
DELETE  /review/{review_id}
🧠 Important Concepts to Explain in an Interview
Before presenting this project, I should be able to explain:
- FastAPI
- REST API
- HTTP methods
- CRUD
- SQLModel
- SQLAlchemy
- Pydantic
- SQLite
- Database engine
- Database session
- Dependency injection
- Depends()
- yield
- Lifespan events
- Request validation
- Response models
- Primary keys
- Database indexes
- Pagination
- Aggregation
- AVG()
- COUNT()
- HTTP 404
- PATCH vs PUT
- commit()
- refresh()
- delete()
- select()
- where()
- offset()
- limit()
🎤 Project Viva Questions
Basic
1. What problem does your project solve?
2. Why did you choose FastAPI?
3. Why did you choose SQLite?
4. What is SQLModel?
5. Explain your project architecture.
6. Explain the request flow from client to database.
7. What are the CRUD operations implemented?
Database
8. What is a database engine?
9. What is a session?
10. Why do you need a session?
11. What is a primary key?
12. Why is play_name indexed?
13. Why use timezone-aware datetime?
14. What happens when session.commit() is called?
15. Why use session.refresh()?
FastAPI
16. What is dependency injection?
17. What does Depends(get_session) do?
18. Why use yield in get_session()?
19. What is a lifespan event?
20. Why use include_router()?
21. What is response_model?
22. What does Query() do?
API Design
23. Why is POST used for creating reviews?
24. Why is GET used for reading reviews?
25. Why is PATCH used for updating reviews?
26. What is the difference between PUT and PATCH?
27. What happens if a review ID does not exist?
28. Why return HTTP 404?
29. Why add pagination?
30. Why calculate average rating using an aggregation query?
🚀 Interview Explanation --- 60 Second Version
"I built a theatre review REST API called Rangmanch Reviews API using
FastAPI, SQLModel and SQLite. The API supports complete CRUD
operations for theatre reviews. I separated the application into
models, database configuration and route modules. SQLModel is used for
both database modeling and validation, while FastAPI handles routing,
request validation and dependency injection. I implemented pagination
using skip and limit, filtering by play name, and an aggregation
endpoint that calculates average rating and total reviews using AVG
and COUNT. Database sessions are provided to routes through FastAPI
dependency injection, and the application creates the required tables
during its lifespan startup event."

📚 Learning Checklist
- [ ] SQLModel for database models
- [ ] SQLite as a zero-configuration database
- [ ] FastAPI lifespan events for startup/shutdown logic
- [ ] Session dependency injection
- [ ] Full CRUD operations
- [ ] Pagination with skip/limit
- [ ] Aggregation queries for average rating
- [ ] Request/response models
- [ ] Error handling with HTTPException
- [ ] Database sessions and transactions
- [ ] API architecture and request flow
💡 Main Learning Goal
The goal of this project is not only to make the API work.
I should be able to explain:
Why am I using this?
        ↓
How does it work?
        ↓
What happens internally?
        ↓
Why is this approach useful?
        ↓
Can I use the same concept in another project?
This README is therefore also my interview preparation and revision
sheet for the Rangmanch Reviews API.
