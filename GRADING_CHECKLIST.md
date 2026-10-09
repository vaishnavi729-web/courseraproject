# Grading Checklist

| Task # | Requirement | Source File / Endpoint | Status | Remaining Action |
| --- | --- | --- | --- | --- |
| 1 | README URL | `README.md` | NEEDS FIX | Validate README formatting and URL location in github. |
| 2 | Django server evidence | `django_server` (Terminal) | NEEDS FIX | Verify DB, run server, capture explicit start output. |
| 3 | About.html URL | `server/frontend/static/About.html` | NEEDS FIX | Ensure proper static layout and commit URL. |
| 4 | Contact Us URL | `.../static/ContactUs.html` | NEEDS FIX | Create correct file (currently missing), commit URL. |
| 5 | Login user evidence | `/login` API | NEEDS FIX | Send correct POST payload, save `userName` JSON response. |
| 6 | Logout user evidence | `/logout` API | NEEDS FIX | Verify logout JSON returns empty `userName`, capture output. |
| 7 | React Register Component | `Register.jsx` URL | NEEDS FIX | Remove syntax errors, implement backend call, commit URL. |
| 8 | Fetch reviews for dealer | `getdealerreviews` | NEEDS FIX | Fix Express server, run cURL, save JSON output. |
| 9 | Fetch all dealers | `getalldealers` | NEEDS FIX | Fetch valid dealership data from Express, save JSON. |
| 10 | Fetch dealer by ID | `getdealerbyid` | NEEDS FIX | Fix Express fallback bug causing fake data, save JSON. |
| 11 | Fetch dealers by State | `getdealersbyState` | NEEDS FIX | Test endpoint, ensure proper filter works, save JSON. |
| 12 | Admin login screenshot | `admin_login.png` | NEEDS FIX | Take correct browser screenshot of Django admin list. |
| 13 | Admin logout screenshot | `admin_logout.png` | NEEDS FIX | Take correct browser screenshot of Django admin logout shell. |
| 14 | Get all car makes | `getallcarmakes` | NEEDS FIX | Implement DB models, query and map data, output JSON. |
| 15 | Sentiment analysis | `analyzereview` | NEEDS FIX | Fix backend connection port and route matching logic, output JSON. |
| 22 | CI/CD success log | `CICD` | NEEDS FIX | Repair `.github/workflows/main.yml`, trigger action, save text log. |
| 23 | Deployment URL | Code Engine Proxy link | NOT INSPECTED | Determine proxy URL structure and verify functionality. |
