# Backend Design for Multi‑Modal Ticketing Platform

$\color{Red}\Huge{\textsf{Huge, colored text}}$
<code style="color: red">N.B: The project is in it's early phase so not much is build</code> <br></br>
This document outlines a modular backend architecture in FastAPI to support various ticket delivery and verification methods. It focuses on clear, robust service layers and pluggable “verification methods” without embedding code examples—defining responsibilities, data flows, and integration points for each approach.

---

## 1. Core Components & Layered Structure

### A. Apps / Feature Modules
- **tickets**: Core ticketing logic (create, read, update, transfer, revoke)
- **verifications**: Abstract interface and registry for verification methods
- **users**: Authentication, authorization, profiles, roles (e.g. staff, admin, attendee)

### B. Shared Core
- **config**: Environment settings and feature flags (enable/disable methods)
- **db**: SQLAlchemy setup, migration control, session management
- **security**: JWT/OAuth2 flows, password hashing
- **dependencies**: `get_db`, `get_current_user`, feature‑toggle injection

### C. Services & Registry
- **VerificationService**: central coordinator that, given a ticket ID and chosen method, routes to the appropriate handler implementation
- **BackgroundTaskManager**: schedules revocation, expiry cleanup, or batch operations (e.g., revoke unscanned tickets)

---

## 2. Verification Methods Interface

Define a common interface with methods like:
- `generate_credential(ticket_id) → payload`  
  Generates unique token, tag data, or pass owner needs.

- `verify_credential(ticket_id, presented_data) → bool`  
  Confirms validity, prevents replay, marks ticket as used/scanned.

Each implementation resides in `apps/verifications/handlers/`.

---

## 3. Handlers Overview

### 3.1 Smartphone‑to‑Smartphone Scanning
- **generate**: Create QR payload containing ticket ID + time‑limited signature.  
- **verify**: On scan, parse QR, verify signature freshness, check ticket not previously used, then mark used.
- **Integration Points**: No hardware API; compatible with any camera‑based mobile app.

### 3.2 NFC / BLE Tap‑and‑Go
- **generate**: Provision an NFC tag record in DB (unique UID → ticket).  
- **verify**: On tap, device sends UID; backend checks mapping, validates state, updates `used_at` timestamp.
- **Lifecycle**: Offer API for on‑site kiosk to write UID to blank wristbands via BLE.

### 3.3 Dynamic Cryptographic Passes
- **generate**: Mint a digital pass (e.g. JWT or signed JSON) with rotating nonce or expiry window.  
- **verify**: Backend verifies signature and nonce against stored `last_seen_nonce` to prevent replay, marks as used.

### 3.4 Blockchain / NFT Tickets
- **generate**: Interact with smart‑contract to mint token; store transaction hash and token ID in DB.  
- **verify**: Query on‑chain state or cache to ensure token ownership and non‑consumption, then update backend state or call smart‑contract to burn/lock token.
- **Fallback**: Mirror on‑chain events in backend for faster reads.

### 3.5 Biometric & Computer‑Vision
- **generate**: On user registration, capture biometric template (face encoding) linked to ticket.  
- **verify**: Accept live face data, run similarity check (on device or via microservice), then confirm match and mark used.  
- **GDPR/Security**: Ensure encrypted storage of biometric data and compliance flags.

### 3.6 Geofencing & Passive Presence
- **generate**: Issue a geofence configuration “entry zone” per event/gate.  
- **verify**: Client SDK sends geofence‑entry webhook; backend matches user ID, ensures single entry event, updates ticket status.

---

## 4. API Endpoints & Flows

### Ticket Lifecycle Endpoints
- **POST /tickets/**: Create ticket
- **GET /tickets/{id}**: Retrieve ticket
- **POST /tickets/{id}/transfer**: Transfer ownership (mark previous credentials invalid)

### Verification Flow Endpoints
- **POST /tickets/{id}/methods**: List available methods (from config flags)
- **POST /tickets/{id}/methods/{method}/generate**: Returns `payload` (QR data, pass file, NFC UID, etc.)
- **POST /tickets/{id}/methods/{method}/verify**: Accepts `presented_data`, returns success or failure

### Admin & Monitoring
- **GET /audits/usage**: View scan history across methods
- **POST /admin/methods/{method}/toggle**: Enable/disable method globally

---

## 5. Data Models & State Tracking

- **Ticket**: core fields + `status` (e.g. created, transferred, used)
- **CredentialRecord**: per‑method records (method_name, credential_id, generated_at, used_at)
- **AuditLog**: granular events (generate, verify, failure reason)

---

## 6. Security & Anti‑Fraud

- **Rate Limiting** on verify endpoints to prevent brute force or replay.
- **Signature Keys Rotation** for dynamic passes.
- **IP & Device Fingerprinting** logs on suspicious usage.
- **Manual Override Endpoints** for staff intervention.

---

## 7. Extensibility & Frontend Choices

Clients can choose any supported method simply by calling the `generate` endpoint for their preferred flow, then submitting the resulting data to `verify`. The backend ensures consistency and single‑use security under the hood, regardless of front‑end implementation.

---

*This design enables a flexible, method‑agnostic ticketing backend that can grow over time with emerging technologies, while providing clear APIs and robust state management.*
