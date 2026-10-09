
import json
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate

from .restapis import (
    get_request,
    analyze_review_sentiments,
    post_review,
)

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body or "{}")
        username = body.get("userName") or body.get("username", "")
        password = body.get("password", "")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user = authenticate(
        request, username=username, password=password
    )

    if user is None:
        return JsonResponse({"userName": username})

    login(request, user)
    return JsonResponse({
        "userName": username,
        "status": "Authenticated"
    })


def logout_request(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body or "{}")
        username = data.get("userName", "").strip()
        password = data.get("password", "")
        email = data.get("email", "")
        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password required"}, status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"error": "Username already exists"}, status=409
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        return JsonResponse({
            "userName": user.username,
            "status": "Registered"
        }, status=201)

    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)


def get_dealerships(request):
    try:
        dealers = get_request("fetchDealers")
        return JsonResponse({"status": 200, "dealers": dealers})
    except Exception:
        logger.exception("Unable to fetch dealers")
        return JsonResponse({"status": 502, "dealers": []}, status=502)


def get_dealerships_by_state(request, state):
    try:
        if state.lower() == "all":
            dealers = get_request("fetchDealers")
        else:
            dealers = get_request(f"fetchDealers/{state}")
        return JsonResponse({"status": 200, "dealers": dealers})
    except Exception:
        logger.exception("Unable to filter dealers")
        return JsonResponse({"status": 502, "dealers": []}, status=502)


def get_dealer_details(request, dealer_id):
    try:
        dealer = get_request(f"fetchDealer/{dealer_id}")
        if not dealer:
            return JsonResponse({"status": 404, "dealer": []}, status=404)
        return JsonResponse({"status": 200, "dealer": [dealer]})
    except Exception:
        logger.exception("Unable to fetch dealer details")
        return JsonResponse({"status": 502, "dealer": []}, status=502)


def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request(f"fetchReviews/dealer/{dealer_id}")
        for review in reviews:
            try:
                result = analyze_review_sentiments(review.get("review", ""))
                review["sentiment"] = result.get("sentiment", "neutral")
            except Exception:
                review["sentiment"] = "neutral"
        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception:
        logger.exception("Unable to fetch dealer reviews")
        return JsonResponse({"status": 502, "reviews": []}, status=502)


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body or "{}")
        required = [
            "name", "dealership", "review", "purchase",
            "purchase_date", "car_make", "car_model", "car_year"
        ]
        if any(key not in data for key in required):
            return JsonResponse(
                {"error": "Missing review fields"}, status=400
            )

        saved = post_review(data)
        return JsonResponse({"status": 200, "review": saved})

    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception:
        logger.exception("Unable to submit review")
        return JsonResponse({"status": 502}, status=502)


def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


def analyze_review(request, text):
    try:
        result = analyze_review_sentiments(text)
        return JsonResponse(result)
    except Exception:
        logger.exception("Sentiment analysis failed")
        return JsonResponse(
            {"error": "Sentiment analyzer unavailable"}, status=502
        )