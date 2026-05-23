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

### Real Payment Gateway Integration
- Stripe payment system integration

## Future Features (Priority Order)

### 1. High Priority (Critical for MVP)
- **Real Payment Gateway Integration:** Include logic for platform service fees, host payouts, and cancellation policies.
- Implement proper cancellation policies and payout for cancelling bookings, with a split of 10% platform fee and the rest to the host.
- **Media Management:** Allow users (hosts) to upload and manage listing images. Implement cloud storage (e.g., AWS S3) and image optimization (resize, compress).
- **Deployment and Infrastructure:** Set up a production environment with Nginx, Gunicorn, PostgreSQL, caching (Redis). Implement CI/CD pipelines and containerize the application using Docker.

### 2. Medium Priority (Important for Enhanced MVP)
- **Advanced Search and Filtering:** Implement map integration for geographical display of listings, dynamic filtering (price range, amenities, rooms/beds, property types), and robust date-based availability search.
- **Advanced Availability Management:** Develop a calendar UI for hosts to easily manage listing availability (block dates, set custom prices) and support time-based bookings.
- **Cancellation Policy Customization:** Allow hosts to define and settle their own cancellation policies.
- **Flexible Payment Options:** Implement a "buy partially now and pay the rest later" option for guests.
- **Real-time Features:** Upgrade the messaging system with WebSockets for live chat and implement real-time notifications for booking requests, messages, etc.

### 3. Lower Priority (Desirable Features)
- **Wishlists & Favorites:** Allow users to save and organize favorite listings.