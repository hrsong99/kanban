# Kanban Board Assignment

## How to run
**macOS:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

If a database file has not been created yet, then before running *python app.py*, follow these steps:
```
python
>>> from app import app, db
>>> app.app_context().push()
>>> db.create_all()
```
This should create a new folder called *Instance* with the file *test.db* inside of it.

## Testing
```bash
python -m unittest discover
```

## Overview
This is the repository for the project. Here's an ovewview of the files:
1. *app.py*: The main python file that houses the logic for Flask and SQLAlchemy
2. *test.py*: The file that hosues the unit tests
3. *base.html*: The base template for the html
4. *index.html*: The main html file for the kanban board
5. *style.css*: The CSS stylesheet that allows the kanban board to look halfway decent
