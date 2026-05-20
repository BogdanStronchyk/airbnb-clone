# Project Backlog

This document outlines features and enhancements planned for future development beyond the initial Minimum Viable Product (MVP).

## Implemented Features (for MVP):

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

## Yet-to-be-implemented Features (for MVP):

### Critical for MVP (High Priority)
1.  **Real Payment Gateway Integration:** Implement a secure, real-world payment gateway (e.g., Stripe/PayPal) to replace the simulated booking process. Include logic for platform service fees, host payouts, and cancellation policies.
2.  **Media Management:** Allow users (hosts) to upload and manage listing images. Implement cloud storage (e.g., AWS S3) and image optimization (resize, compress).

### Important for Enhanced MVP (Medium Priority)
3.  **Advanced Search and Filtering:** Implement map integration for geographical display of listings, dynamic filtering (price range, amenities, rooms/beds, property types), and robust date-based availability search.
4.  **Advanced Availability Management:** Develop a calendar UI for hosts to easily manage listing availability (block dates, set custom prices) and support time-based bookings.
5.  **Real-time Features:** Upgrade the messaging system with WebSockets for live chat and implement real-time notifications for booking requests, messages, etc.

### Desirable Features (Lower Priority)
6.  **Wishlists & Favorites:** Allow users to save and organize favorite listings.

### Essential for Production Deployment (High Priority - Infrastructure)
7.  **Deployment and Infrastructure:** Set up a production environment with Nginx, Gunicorn, PostgreSQL, caching (Redis). Implement CI/CD pipelines and containerize the application using Docker.
