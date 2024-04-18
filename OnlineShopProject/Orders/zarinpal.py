from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import json

# Determine the sandbox or production environment
sandbox = 'sandbox'

# API endpoints
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# Payment details
amount = 1000
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
phone = 'YOUR_PHONE_NUMBER' 
CallbackURL = 'http://127.0.0.1:8080/verify/' 

class PaymentRequestAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            "MerchantID": 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
            "Amount": amount,
            "Description": description,
            "Phone": phone,
            "CallbackURL": CallbackURL,
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(ZP_API_REQUEST, json=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return Response({'status': True, 'url': ZP_API_STARTPAY + str(response_data['Authority']), 'authority': response_data['Authority']})
            else:
                return Response({'status': False, 'code': str(response_data['Status'])}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': False, 'code': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentVerificationAPI(APIView):
    def post(self, request, *args, **kwargs):
        authority = request.data.get('authority')
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Authority": authority,
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(ZP_API_VERIFY, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return Response({'status': True, 'RefID': response_data['RefID']})
            else:
                return Response({'status': False, 'code': str(response_data['Status'])}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': False, 'code': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)