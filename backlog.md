# Project Backlog

This document outlines features and enhancements planned for future development beyond the initial Minimum Viable Product (MVP).

## 1. Advanced Search and Filtering
- **Map Integration**: Implement a map view (e.g., using Mapbox or Google Maps) to display listings geographically.
- **Dynamic Filtering**: Add filters for price range, specific amenities, number of rooms/beds, and property types.
- **Date-based Availability Search**: Ensure search results only show listings available for the selected dates.

## 2. Advanced Availability Management
- **Calendar UI for Hosts**: Provide a calendar interface for hosts to manage their listing availability (block dates, set custom prices).
- **Time Slots**: Support time-based bookings (e.g., hourly for tours or experiences), not just daily bookings.

## 3. Real Payment Gateway Integration
- **Stripe/PayPal Integration**: Replace the simulated booking process with a secure, real-world payment gateway.
- **Service Fees**: Implement logic for platform service fees and host payouts.
- **Cancellation Policies**: Support different cancellation policies (flexible, moderate, strict) and automate refunds.

## 4. Enhanced User Profiles
- **User Verification**: Implement identity verification (ID upload, phone number verification) to increase trust.
- **Host Dashboard**: Create a dedicated dashboard for hosts to track earnings, view upcoming bookings, and manage listings efficiently.
- **Profile Reviews**: Display overall ratings and reviews on user profiles, not just on listings.

## 5. Media Management
- **Image Uploads**: Allow users (hosts) to upload images directly to the platform (using cloud storage like AWS S3).
- **Image Optimization**: Automatically resize and compress uploaded images for better performance.

## 6. Real-time Features
- **Live Messaging**: Upgrade the basic messaging system to use WebSockets (e.g., Django Channels) for instant message delivery without page reloads.
- **Real-time Notifications**: Notify users instantly about new booking requests, messages, or review submissions.

## 7. Wishlists & Favorites
- **Save Listings**: Allow users to save favorite listings to customized wishlists for future reference.

## 8. Deployment and Infrastructure
- **Production Environment setup**: Configure Nginx, Gunicorn, PostgreSQL, and a robust caching layer (e.g., Redis).
- **CI/CD Pipeline**: Implement continuous integration and deployment workflows.
- **Containerization**: Use Docker to containerize the application for consistent deployments.
