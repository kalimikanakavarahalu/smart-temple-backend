# Smart Temple Solution — Backend, GitHub Setup & Agent Inventory Plan
*Based on: Proposal_for_Smart_Temple_Solution.pdf (Ixicities)*

## 1. Backend Initial Setup (Today)

### 1.1 Tech Stack Decision
| Layer | Recommended | Alternative |
|-------|-------------|-------------|
| **API Framework** | Node.js + Express/NestJS | Python + FastAPI |
| **Database (transactional)** | PostgreSQL | MySQL |
| **Database (events/streaming)** | MongoDB / TimescaleDB | InfluxDB |
| **Cache / Queue** | Redis + BullMQ | RabbitMQ |
| **AI/ML serving** | Python microservices (FastAPI) | — |
| **Blockchain ledger** | Hyperledger Fabric / Polygon (private) | Simple append-only signed log |
| **Auth** | JWT + OAuth2 (staff, VIP, devotee) | Keycloak |
| **File/Media storage** | S3-compatible (MinIO for self-host) | Firebase Storage |
| **Real-time** | WebSockets / MQTT (IoT & drones) | Socket.io |

### 1.2 Project Folder Structure
```text
smart-temple-backend/
├── src/
│   ├── api/             # REST controllers (per module)
│   ├── agents/          # AI agent microservices/orchestration logic
│   ├── services/        # business logic
│   ├── models/          # DB schemas
│   ├── jobs/            # cron/queue workers
│   ├── integrations/    # IoT, drone, payment, blockchain
│   ├── middleware/      # auth, logging, error handling
│   ├── config/
│   └── utils/
├── tests/
├── docker-compose.yml
├── .env.example
├── package.json / requirements.txt
└── README.md
```

### 1.3 Today's Action Items
- [ ] `git init` + push to GitHub (see Section 2).
- [ ] Set up `docker-compose.yml` with Postgres + Redis + MongoDB.
- [ ] Create base Express/FastAPI app with health-check route.
- [ ] Create `.env.example` with `DB_URL`, `JWT_SECRET`, `REDIS_URL`.
- [ ] Define core DB entities: `Users`, `Staff`, `Devotees`, `Roles`, `Assets`, `Donations`, `DarshanPermissions`, `Bookings`, `Devices`, `Alerts`, `CrowdEvents`.
- [ ] Stub out one working endpoint per core module to validate setup (e.g., `/api/health`, `/api/auth/login`).

---

## 2. GitHub Setup

### 2.1 Repository Strategy
Recommend mono-repo with workspaces (easier for a single team at MVP stage):
```text
smart-temple/
├── backend/                   # core API
├── agents/                    # individual AI agent services (can be split later)
├── frontend-devotee-app/
├── frontend-admin-dashboard/
└── infra/                     # docker, k8s, CI configs
```

### 2.2 Branching Model
- `main` → production
- `develop` → integration branch
- `feature/<module-name>` → e.g. `feature/darshan-permissions`, `feature/asset-tracker`
- PRs require 1 review + passing CI before merge into `develop`.

### 2.3 Repo Hygiene
- `.gitignore` (node_modules, .env, pycache, dist)
- `README.md` with setup instructions
- Issue templates: Bug report, Feature request
- PR template with checklist (tests, docs, env vars updated)
- GitHub Projects board with columns: Backlog → In Progress → Review → Done (one card per page/module).

### 2.4 CI (GitHub Actions) — minimal starter
```yaml
name: CI
on: [push, pull_request]
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

---

## 3. Page-wise Agent / Module Inventory (Full Coverage)
*Goal: every page of the proposal maps to concrete backend modules, AI agents, and tech stacks.*

| Pg | Feature | Agent(s) / Module(s) Needed | Type | Libraries / Tech | API Keys & DB |
|----|---------|-----------------------------|------|------------------|---------------|
| **2-3** | Intro & Challenges | Concept overview | Info | — | — |
| **4** | Smart Temple Framework | Orchestrator Agent (routes events between all agents) | Core | `Kafka` / `Redis PubSub` | Redis |
| **5** | AI & Robotics | Devotee Assistant, Queue Mgmt, Resource Allocation Agent | AI | `langchain`, `ROS` | OpenAI/Gemini API |
| **6** | IoT & Drones | IoT Telemetry, Drone Surveillance, Security Alert Agent | AI/IoT | `paho-mqtt`, `TensorFlow` | Twilio API, InfluxDB |
| **7** | Video & Predictive | Crowd Video Analytics, Predictive Forecasting Agent | AI | `YOLOv8`, `OpenCV` | MongoDB |
| **8** | Smart Darshan | Permission Request, QR Gen, VIP Authorization Agent | Core+AI | `qrcode`, `jsonwebtoken` | SendGrid (Email), Postgres |
| **9** | Staff & Asset Tracker | Attendance Logging, Asset Tracking, Theft Detection Agent | Core/IoT | `pyserial`, NFC/RFID SDKs | FCM (Push), Postgres |
| **10** | Disaster Early Warning | Crowd Risk Agent, Auto-Rerouting, Emergency Dispatch Agent | AI (Critical) | `PyTorch`, `scikit-learn` | Public Announce API, Redis |
| **11** | Digital Twin | Simulation/Digital-Twin Agent | AI/Sim | `Three.js`, `WebSockets` | MongoDB |
| **12** | VIP Protocol Mgmt | VIP Route Optimization, Escort Coordination Agent | AI | `NetworkX` | Google Maps API, Postgres |
| **13** | Queue Sentiment | Sentiment Detection, Escalation Agent | AI | `DeepFace` / `FER` | Postgres, Redis |
| **14** | Prasadam Forecast | Demand Forecasting Agent (uses crowd/weather data) | AI | `prophet`, `pandas` | OpenWeatherMap API |
| **15** | Digital Donations | Donation Processing, Blockchain Ledger Agent | Core/Block | `web3.js`, Stripe/Razorpay | Payment API, Hyperledger |
| **16** | Crowd Mgmt/Face ID | Crowd Flow, Face Recognition, Incident Reporting Agent | AI (Sensitive) | `face_recognition`, `dlib` | ChromaDB/Faiss |
| **17** | Kiosks & Pooja Booking | Kiosk Dispensing, Pooja Booking, Hotel Booking Integration | Core/Int | `React.js` | Oyo/MakeMyTrip APIs |
| **18** | Devotees App | Devotee Guide, Notification, Map/Navigation Agent | Core/AI | `React Native` / `Flutter` | Google Maps API |
| **19-20** | Impl. Plan & PPP | Project management and Business model | Info | — | — |
| **21** | Benefits Summary | Reporting/Analytics Agent (pulls from all agents) | Core | `Grafana` / `Metabase` | Data Warehouse |

### 3.1 Cross-Cutting Agents (Build Once, Reuse)
- **Auth & RBAC Agent** — Devotee / staff / VIP / admin roles.
- **Notification Agent** — SMS/push/app alerts (used by pages 6, 10, 13, 17, 18).
- **Event Bus / Orchestrator Agent** — Connects IoT, video, drones, AI agents.
- **Audit & Reporting Agent** — Feeds dashboards for pages 9, 15, 21.

### 3.2 Suggested Build Order (MVP → Advanced)
1. **Auth + Devotee App basics** (Pages 2, 4, 18)
2. **Darshan Permissions + QR** (Page 8)
3. **Staff Attendance & Asset Tracker** (Page 9)
4. **Donations & Ledger** (Page 15)
5. **Crowd Video Analytics + Stampede Warning** (Pages 7, 10) — *High-impact, needs camera infra.*
6. **IoT/Drones** (Page 6) — *Needs hardware procurement first.*
7. **Predictive/Sentiment/Digital Twin** (Pages 11, 13, 14) — *Data-heavy, build after enough historical data.*
8. **Face ID/Offender detection** (Page 16) — *Flag for legal/privacy review before build.*

✅ **Coverage Check**: All 22 pages mapped. Informational pages intentionally have no agent; all functional pages have at least one named agent/module alongside technical stack details.
