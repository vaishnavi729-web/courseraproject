# Evidence Manifest

This directory contains all the evidence required for the final assessment grading:

## Log Files
* `../CICD` - Log output of successful Github Actions python/js linting.
* `../deploymentURL` - Document explaining limitations of proxy generation in the offline environment.
* `../django_server` - Startup log of the Django backend on port 8000.

## Endpoint Response Outputs
* `../loginuser` - JSON response for successful authentication with root credentials.
* `../logoutuser` - JSON response for logout endpoint.
* `../getalldealers` - JSON response fetching all dealership documents.
* `../getdealerbyid` - JSON response fetching dealer ID #1.
* `../getdealersbyState` - JSON response fetching Kansas dealerships.
* `../getdealerreviews` - JSON array of reviews for dealer #1.
* `../getallcarmakes` - JSON response matching SQLite CarModels and CarMakes.
* `../analyzereview` - JSON output for sentiment intensity matching text string.

## UI Screenshots (`/screenshots`)
* `admin_login.png` - Django administration login panel
* `admin_logout.png` - Django administration logged out panel
* `contact_us.png` - Repaired frontend layout containing Contact details and fixed images
* `get_dealers.png` - Dealership list view (anonymous)
* `get_dealers_loggedin.png` - Dealership list view (authenticated via login route)
* `dealersbystate.png` - Filtered Kansas dealerships 
* `dealer_id_reviews.png` - Reviews container for single dealer
* `dealership_review_submission.png` - Adding a review form with populated fields
* `added_review.png` - Redirect to dealer page showing the newly posted review
