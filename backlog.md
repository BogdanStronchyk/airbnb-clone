# Project Backlog

This document outlines features and enhancements planned for future development beyond the initial Minimum Viable Product (MVP).

## Implemented Features

### User Authentication and Profiles
- User registration, login, logout
- User profiles
- Becoming a host
- User Reviews (for hosts)

### Listing Management
- Creating, editing, viewing listings
- Service categories
- Host dashboard

### Search and Filtering
- Basic search
- Listing detail view

### Booking System
- Booking creation
- Trips view for users
- Booking approval/denial by host
- Reviews for bookings

### Messaging
- Basic messaging system
- Inbox and conversation views

### Availability Management
- Setting availability for listings

## Future Features (Priority Order)

### 1. High Priority (Critical for MVP)
- **Real Payment Gateway Integration:** Implement a secure, real-world payment gateway (e.g., Stripe/PayPal) to replace the simulated booking process. Include logic for platform service fees, host payouts, and cancellation policies.
- **Media Management:** Allow users (hosts) to upload and manage listing images. Implement cloud storage (e.g., AWS S3) and image optimization (resize, compress).
- **Deployment and Infrastructure:** Set up a production environment with Nginx, Gunicorn, PostgreSQL, caching (Redis). Implement CI/CD pipelines and containerize the application using Docker.

### 2. Medium Priority (Important for Enhanced MVP)
- **Advanced Search and Filtering:** Implement map integration for geographical display of listings, dynamic filtering (price range, amenities, rooms/beds, property types), and robust date-based availability search.
- **Advanced Availability Management:** Develop a calendar UI for hosts to easily manage listing availability (block dates, set custom prices) and support time-based bookings.
- **Real-time Features:** Upgrade the messaging system with WebSockets for live chat and implement real-time notifications for booking requests, messages, etc.

### 3. Lower Priority (Desirable Features)
- **Wishlists & Favorites:** Allow users to save and organize favorite listings.