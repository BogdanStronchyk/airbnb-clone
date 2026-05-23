from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import ServiceListing
from .models import Booking
from unittest.mock import patch, MagicMock
import json

User = get_user_model()

class StripeTransactionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.provider = User.objects.create_user(username='provider', password='password', is_provider=True)
        self.customer = User.objects.create_user(username='customer', password='password')
        self.listing = ServiceListing.objects.create(
            provider=self.provider,
            title='Test Listing',
            description='Test Description',
            base_price=100.00
        )
        self.booking = Booking.objects.create(
            customer=self.customer,
            listing=self.listing,
            start_date='2024-01-01',
            end_date='2024-01-05',
            total_price=400.00,
            stripe_payment_intent_id='pi_test_123',
            payment_status='pending',
            status='pending'
        )
        self.webhook_url = reverse('stripe_webhook')  # Ensure you have this name in urls.py

    @patch('stripe.PaymentIntent.create')
    @patch('stripe.Webhook.construct_event')
    def test_payment_creation_and_success_flow(self, mock_construct_event, mock_pi_create):
        print("\n--- Starting Test: Payment Creation -> Success Flow ---")
        # 1. Simulate Booking Creation (PaymentIntent creation)
        self.client.force_login(self.customer)
        mock_pi = MagicMock()
        mock_pi.id = 'pi_integration_success_123'
        mock_pi.client_secret = 'secret_success_123'
        mock_pi_create.return_value = mock_pi

        booking_data = {
            'listing': self.listing.id,
            'start_date': '2024-02-01',
            'end_date': '2024-02-05',
            'total_price': '400.00'
        }
        
        print("  -> Simulating Booking Creation Request to API...")
        response = self.client.post(
            reverse('booking-list'), # Assuming default router name
            data=booking_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        created_booking_id = response.json()['id']
        print(f"  -> Booking created successfully. ID: {created_booking_id}")
        
        # Verify initial state
        booking = Booking.objects.get(id=created_booking_id)
        self.assertEqual(booking.payment_status, 'pending')
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.stripe_payment_intent_id, 'pi_integration_success_123')

        # 2. Simulate Webhook Event (PaymentIntent succeeded)
        print("  -> Simulating incoming Webhook: payment_intent.succeeded...")
        mock_event = MagicMock()
        mock_event.type = 'payment_intent.succeeded'
        mock_event.data.object.id = 'pi_integration_success_123'
        mock_construct_event.return_value = mock_event

        payload = {'type': 'payment_intent.succeeded'}
        response = self.client.post(
            self.webhook_url,
            json.dumps(payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )
        self.assertEqual(response.status_code, 200)

        # Verify final state
        booking.refresh_from_db()
        self.assertEqual(booking.payment_status, 'succeeded')
        self.assertEqual(booking.status, 'confirmed')
        print("  -> Verification: Booking payment_status updated to 'succeeded' and status to 'confirmed'.")
        print("--- End Test ---\n")

    @patch('stripe.PaymentIntent.create')
    @patch('stripe.Webhook.construct_event')
    def test_payment_creation_and_failure_flow(self, mock_construct_event, mock_pi_create):
        print("\n--- Starting Test: Payment Creation -> Failure Flow ---")
        # 1. Simulate Booking Creation (PaymentIntent creation)
        self.client.force_login(self.customer)
        mock_pi = MagicMock()
        mock_pi.id = 'pi_integration_fail_123'
        mock_pi.client_secret = 'secret_fail_123'
        mock_pi_create.return_value = mock_pi

        booking_data = {
            'listing': self.listing.id,
            'start_date': '2024-03-01',
            'end_date': '2024-03-05',
            'total_price': '400.00'
        }
        
        print("  -> Simulating Booking Creation Request to API...")
        response = self.client.post(
            reverse('booking-list'),
            data=booking_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        created_booking_id = response.json()['id']
        print(f"  -> Booking created successfully. ID: {created_booking_id}")

        # Verify initial state
        booking = Booking.objects.get(id=created_booking_id)
        self.assertEqual(booking.payment_status, 'pending')
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.stripe_payment_intent_id, 'pi_integration_fail_123')

        # 2. Simulate Webhook Event (PaymentIntent failed)
        print("  -> Simulating incoming Webhook: payment_intent.payment_failed...")
        mock_event = MagicMock()
        mock_event.type = 'payment_intent.payment_failed'
        mock_event.data.object.id = 'pi_integration_fail_123'
        mock_construct_event.return_value = mock_event

        payload = {'type': 'payment_intent.payment_failed'}
        response = self.client.post(
            self.webhook_url,
            json.dumps(payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )
        self.assertEqual(response.status_code, 200)

        # Verify final state
        booking.refresh_from_db()
        self.assertEqual(booking.payment_status, 'failed')
        self.assertEqual(booking.status, 'cancelled')
        print("  -> Verification: Booking payment_status updated to 'failed' and status to 'cancelled'.")
        print("--- End Test ---\n")

    @patch('stripe.Webhook.construct_event')
    def test_payment_intent_succeeded(self, mock_construct_event):
        # Mock the event returned by construct_event
        mock_event = MagicMock()
        mock_event.type = 'payment_intent.succeeded'
        mock_event.data.object.id = 'pi_test_123'
        mock_construct_event.return_value = mock_event

        payload = {'type': 'payment_intent.succeeded'}
        
        response = self.client.post(
            self.webhook_url,
            json.dumps(payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )
        
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.payment_status, 'succeeded')
        self.assertEqual(self.booking.status, 'confirmed')

    @patch('stripe.Webhook.construct_event')
    def test_payment_intent_failed(self, mock_construct_event):
        # Mock the event returned by construct_event
        mock_event = MagicMock()
        mock_event.type = 'payment_intent.payment_failed'
        mock_event.data.object.id = 'pi_test_123'
        mock_construct_event.return_value = mock_event

        payload = {'type': 'payment_intent.payment_failed'}
        
        response = self.client.post(
            self.webhook_url,
            json.dumps(payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )
        
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.payment_status, 'failed')
        self.assertEqual(self.booking.status, 'cancelled')
