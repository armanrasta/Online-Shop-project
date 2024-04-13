import requests
import json

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید" 
phone = 'YOUR_PHONE_NUMBER'
CallbackURL = 'http://127.0.0.1:8080/order/verify/'

def send_request(amount, description, phone, CallbackURL):
    data = {
        "MerchantID": 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
   
    headers = {'content-type': 'application/json'}
    try:
        response = requests.post(ZP_API_REQUEST, json=data, headers=headers, timeout=10)
        response_data = response.json()

        if response.status_code == 200 and response_data['Status'] == 100:
            return {'status': True, 'url': ZP_API_STARTPAY + str(response_data['Authority']), 'authority': response_data['Authority']}
        else:
            return {'status': False, 'code': str(response_data.get('Status', 'error'))}
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}
    except requests.exceptions.RequestException as e:
        return {'status': False, 'code': 'request exception', 'message': str(e)}