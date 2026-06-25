# Smart Temple Solution - Complete Workflow Documentation

## 1. Project Overview
The **Smart Temple Backend** is a next-generation temple management system built with **FastAPI (Python)**. It integrates **Artificial Intelligence (AI)**, **IoT simulations**, and **Data Analytics** to modernize temple operations. 

The primary goals of this system are:
- Automating Devotee Darshan bookings with AI-based decision making.
- Tracking temple assets securely using IoT (RFID) and AI anomaly detection.
- Processing E-Hundi donations securely with AI fraud detection and blockchain-style ledgers.
- Ensuring devotee safety through AI-powered crowd analytics and emergency evacuation protocols.

---

## 2. Role-Based Access Control (RBAC)
The system operates on strict role-based permissions to ensure data security and operational integrity:
- **Admin**: Has overarching access. Can register new assets, view all security alerts, and monitor crowd feeds.
- **Staff (Security/Temple Staff)**: Can scan devotee QR codes at the entrance, track asset movements (RFID scanning), and trigger emergency evacuations.
- **Devotee**: Can register/login, manage their profile, book Darshan tickets, and make donations.

*(Note: All API responses follow a standardized JSON format containing `success`, `message`, `data`, and `errors` fields for seamless Frontend integration).*

---

## 3. End-to-End Module Workflows

### A. Authentication & Security Workflow
1. **Registration**: A user registers via `/api/auth/register`. Their password is encrypted immediately using **Bcrypt Hashing** before being saved to the database.
2. **Login**: The user logs in via `/api/auth/login` and receives an **OAuth2 JWT Access Token**. This token is used to authenticate all subsequent requests.
3. **Forgot Password**: 
   - User requests a reset via `/api/auth/forgot-password`.
   - System generates a 6-digit OTP (valid for 10 minutes) and sends it to the user's email.
   - User verifies the OTP via `/api/auth/verify-otp` and receives a unique `reset_token`.
   - User submits the `reset_token` and new password to `/api/auth/reset-password` to complete the process.

### B. Darshan Booking & QR System Workflow
1. **Darshan Request**: A devotee requests a Darshan slot for a specific date and time (`/api/darshan/request`).
2. **AI Evaluation (`permission_agent.py`)**: Before confirming the booking, the AI agent evaluates the request based on rules (e.g., VIPs get priority, maximum bookings per day, special event restrictions).
3. **QR Generation**: If the AI approves the request, the system generates a secure, base64-encoded **QR Code** containing the devotee's booking details and stores it in the database.
4. **Temple Entry (Scanning)**: When the devotee arrives at the temple, **Staff** use the `/api/darshan/scan` endpoint to scan the QR code. The system verifies the QR data, marks the Darshan as 'completed', and allows entry.

### C. Asset Management & IoT Tracking Workflow
1. **Registration**: The **Admin** registers a temple asset (e.g., Gold Jewellery, Keys, Hundi) via `/api/assets/register` and assigns it a unique **RFID Tag**.
2. **Movement Tracking (IoT Simulator)**: When the asset is moved, an RFID scanner at the doorway automatically triggers the `/api/assets/simulator/scan` endpoint.
3. **AI Security Check (`asset_agent.py`)**: The AI agent analyzes the movement. If an asset is moved to an unauthorized location (e.g., "Jewellery" moved to "Outside Gate"), the AI flags it as a "High Severity Theft Risk" and generates a security alert.
4. **Alerts Dashboard**: Admins can fetch active anomalies via `/api/assets/alerts`.

### D. E-Hundi & Donations Workflow
1. **Making a Donation**: A devotee submits a donation via `/api/donations/process`.
2. **AI Fraud Detection (`donation_agent.py`)**: The AI agent analyzes the transaction in real-time. If the amount is unusually large or suspicious, it flags the transaction for manual KYC review and blocks it.
3. **Blockchain Ledger**: Once cleared by the AI, the payment is processed. The system generates a cryptographic **Hash** (simulating a Blockchain Ledger) to ensure the donation record is immutable and transparent.
4. **History**: Devotees can view their past donations via `/api/donations/history/{user_id}`.

### E. Crowd Analytics & Emergency Workflow
1. **CCTV Integration (IoT Simulator)**: Temple CCTV cameras continuously send estimated headcounts of different temple zones to `/api/crowd/simulator/camera_feed`.
2. **AI Density Analysis (`crowd_agent.py`)**: The AI analyzes the headcount against the zone's maximum capacity. If a zone exceeds 90% capacity, it automatically triggers a "Stampede Warning".
3. **Emergency Evacuation**: If a critical situation arises, **Staff/Admin** can trigger `/api/crowd/evacuation`. In a real-world scenario, this would broadcast dynamic exit routes and push notifications to the mobile apps of all devotees currently in that specific zone.

---

## 4. Technology Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite (Development) / SQLAlchemy ORM
- **Security**: JWT (JSON Web Tokens), Bcrypt Password Hashing, OAuth2
- **AI Integration**: Custom Python Agents (Modular rule-based and predictive simulators)
- **Data Validation**: Pydantic

## 5. How to Test Locally
1. Run the server: `python -m uvicorn main:app --reload`
2. Open the Interactive API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`
3. Use the **Authorize** button at the top to login and inject your JWT token to test role-restricted endpoints.
