# flask-react-comments


## **Project Overview**

This project is a full-stack web application to **add, edit, delete, and view comments** for a given task. It demonstrates **CRUD operations** using a Flask backend and a React frontend. The application also includes automated tests for backend APIs.

---

## **Features**

* Add comments to a task with optional author name
* Edit existing comments
* Delete comments
* View all comments for a specific task
* Backend API tested using `pytest`
* Frontend integrated with backend using **Axios** and **fetch**

---

## **Tech Stack**

* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS
* **Frontend:** React, Axios
* **Database:** SQLite (development)
* **Testing:** Pytest (backend API tests)
---

## **Project Structure**

```
backend/           # Flask backend
 ├── app/
 │   ├── __init__.py
 │   ├── comments.py
 │   ├── config.py
 │   ├── models.py
 │
 ├── run.py
 └── tests/
     └── test_comments.py

frontend/          # React frontend
 ├── src/
 │   ├── components/
 │   │   └── Comments.jsx
 │   ├── index.js
 │   └── App.js
 └── package.json
```

---

## **Setup Instructions**

### Backend

1. Create and activate virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the backend:

```bash
python run.py
```

The backend runs at `http://localhost:5000/`.

4. Run automated tests:

```bash
pytest
```

### Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start frontend development server:

```bash
npm start
```

The frontend runs at `http://localhost:3000/`.

---

## **API Endpoints**

| Method | Endpoint                       | Description                 |
| ------ | ------------------------------ | --------------------------- |
| POST   | `/api/comments/`               | Create a new comment        |
| GET    | `/api/comments/task/<task_id>` | Get all comments for a task |
| PUT    | `/api/comments/<comment_id>`   | Update a comment            |
| DELETE | `/api/comments/<comment_id>`   | Delete a comment            |


