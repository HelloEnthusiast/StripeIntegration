import stripe
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY  

def payment_page(request):
    return render(request, 'payment.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body) 
            amount = int(float(data['amount']) * 100)  
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Donation to Jarkar Officials',
                            },
                            'unit_amount': amount,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def success_view(request):
    return render(request, 'success.html')

def cancel_view(request):
    return render(request, 'cancel.html')

import datetime

def download_receipt(request):
    receipt_content = f"""
    Receipt
    ---------
    Transaction ID: 1234567890
    Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Amount Paid: $50.00
    Status: Successful
    Thank you for your payment!
    """

    response = HttpResponse(receipt_content, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="Receipt.txt"'
    return response