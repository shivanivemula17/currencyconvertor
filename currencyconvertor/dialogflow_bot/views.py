from django.shortcuts import render
import json
import requests
from django.http import JsonResponse


# Create your views here.


# Function to fetch real-time currency conversion rates
def convert_currency(amount, from_currency, to_currency):
    api_key = "your_api_key"  # Use an API like exchangerate-api.com or forex API
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    
    response = requests.get(url)
    data = response.json()

    if to_currency in data['rates']:
        converted_amount = amount * data['rates'][to_currency]
        return round(converted_amount, 2)
    else:
        return None

# Webhook view for Dialogflow fulfillment
def dialogflow_webhook(request):
    req = json.loads(request.body)
    
    if req.get("queryResult"):
        query_text = req["queryResult"]["queryText"]
        parameters = req["queryResult"]["parameters"]
        from_currency = parameters["unit-currency"]["currency"]
        to_currency = parameters["currency-name"]
        amount = parameters["unit-currency"]["amount"]

        # Convert currency
        converted_amount = convert_currency(amount, from_currency, to_currency)

        if converted_amount is not None:
            fulfillment_text = f"{amount} {from_currency} is {converted_amount} {to_currency}."
        else:
            fulfillment_text = "Sorry, I couldn't process your request."

        return JsonResponse({"fulfillmentText": fulfillment_text})

    return JsonResponse({"fulfillmentText": "Invalid request."})


