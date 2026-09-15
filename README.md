# Cookzilla

Cookzilla is a feature-rich Flask web application designed for sharing recipes, managing culinary communities, and organizing cooking events backed by a MySQL database.

---

## Features

### User Authentication & Settings
* **Authentication:** Secure login and registration system to authenticate users before granting access to protected routes.
* **Unit Preferences:** Set preferred measurement units and convert units within recipes automatically.

### Recipe Management & Discovery
* **Post & Build Recipes:** Create recipes with incrementally added steps, ingredients, and components.
* **Media Support:** Upload and display images during the recipe creation (`create-recipe`) flow.
* **Reviews & Ratings:** Post reviews and rate recipes.
* **Simple & Advanced Search:** Search recipes by tags, star ratings, or complex multi-criteria queries.
* **Detailed Recipe Views:** Display detailed instructions, ordered steps, and ingredient lists.

### Groups & Community Events
* **Group Management:** Create new groups or join existing cooking communities.
* **Event Creation:** Group members can create events tailored to their specific groups.
* **RSVP System:** Group members can RSVP to upcoming events.

---

## File Architecture

| File | Description |
| :--- | :--- |
| `Create_group.py` | Handles group creation logic for users. |
| `Join_group.py` | Manages requests for users to join existing groups. |
| `Create_event.py` | Enables group members to create and publish events. |
| `Rsvp.py` | Handles event RSVP functionality for group members. |
| `Event.py` | Controller for rendering backend event data into `event.html`. |
| `init1.py` | Main Flask application entry point and routing controller. |
| `DB_Project/FlaskDemo.sql` | Database table creation scripts and schema definition. |

---

## Getting Started

### Prerequisites
* **Python 3.x**
* **MySQL Server** & **MySQL Workbench** (or compatible client)

### Environment Setup

1. **Navigate to the project directory:**
   ```bash
   cd DB_Project

   Create and activate a virtual environment:

Bash
python3 -m venv venv
source venv/bin/activate
(Run deactivate whenever you need to exit the virtual environment.)

Install dependencies:

Bash
pip3 install -r requirements.txt
Database Setup
Open MySQL Workbench (or your preferred database application).

Create a database named FlaskDemo.

Open and run the table creation queries located in DB_Project/FlaskDemo.sql against the FlaskDemo database.

Running the Application
Set the Flask environment variables and start the server:

Bash
export FLASK_APP=init1.py
export FLASK_ENV=development
flask run
Open your browser and navigate to:

Plaintext
[http://127.0.0.1:5000](http://127.0.0.1:5000)
