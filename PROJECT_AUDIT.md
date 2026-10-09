# Project Audit

## Architecture Summary
- **Backend (Django):** `server/djangoapp` handles standard user workflows, authentication, and routing logic. Needs to define DB models for CarMake/CarModel.
- **Backend (Express):** `server/database/app.js` handles dealership data queries on port 3000.
- **Microservice (Flask):** `server/djangoapp/microservices/app.py` handles sentiment analysis with `nltk`, typically running on port 5050 or 5000.
- **Frontend (React/Static):** Static pages exist for Home, About, but `Contact*.html` is missing. React manages user registration but has syntax errors and isn't wired to the backend properly.

## Defect Findings
1.  **Missing Contact Us Page:** `Contact.html` or `ContactUs.html` does not exist in `server/frontend/static/`. It must be created and linked correctly.
2.  **React Registration Component:** `server/frontend/src/components/Register/Register.jsx` contains literal markdown backticks inside the javascript file, resulting in invalid syntax. It also lacks backend API integration (currently an empty stub).
3.  **Missing Django Models:** `server/djangoapp/models.py` only has hints and comments. `CarMake` and `CarModel` definitions are completely missing.
4.  **Hardcoded Cars API:** `views.get_cars` in Django returns a hardcoded array of dictionaries rather than querying the SQL database. 
5.  **Express Fallback Masking 404:** `fetchDealer/:id` returns `dealerships_data[0]` if an ID is missing, returning misleading data instead of correctly handling missing records.
6.  **Sentiment Analyzer Routing mismatch:** `app.js` routes `/analyze/:text` to `http://127.0.0.1:5000/analyze/...` while `restapis.py` expects the service at port `5050`.

## Recommended Repair Order
1.  **Static Pages & Frontend Logic:** Create `server/frontend/static/ContactUs.html`. Fix the buggy `Register.jsx` syntax and implement registration submission logic.
2.  **Database & Django Models:** Define `CarMake` and `CarModel` in `models.py`, generate and apply migrations. Remove hardcoded arrays from `views.py`.
3.  **Express & Flask Endpoints:** Correct Express route bugs in `app.js` (port and missing handling configurations). Test sentiment integrations locally.
4.  **Run Pipeline:** Start the various backend servers (Django, Express, Flask) and verify integration is flawless.
5.  **CI/CD Repair:** Fix GitHub Actions workflow (`main.yml`), push to GitHub to run CI properly and generate the log.
6.  **Evidence Generation:** Safely run each script and capture exact expected textual and visual evidence for Final Submission.
