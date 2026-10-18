# Darell Rangga Putra Rachman
### Software Engineer · Machine Learning & Systems Architect
**Information Systems (GPA: 4.00 / 4.00) · 1st Place Champion IT Boot Camp 2026**

<p align="left">
  <a href="https://linkedin.com/in/darellrangga"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://darellrangga.me"><img src="https://img.shields.io/badge/Portfolio-24292F?style=flat-square&logo=googlechrome&logoColor=white" alt="Portfolio" /></a>
  <a href="https://github.com/Rangga11268"><img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="mailto:darrelrangga@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
</p>

---

## Overview

I build production-grade server-side software, vectorized mathematical machine learning engines, and distributed web applications. My engineering philosophy prioritizes **first-principles implementation over black-box wrappers**: optimizing memory layouts, managing concurrency bottlenecks, and eliminating compute overheads directly at the algorithmic and database levels.

Key highlights across my codebase:
- **500+ Automated Unit Tests:** Maintaining 100% pass rates across local and production suites (Pytest, PHPUnit, Ragas).
- **Zero-Docker Native Performance:** All machine learning engines run at sub-millisecond to sub-25ms CPU latencies using pure SIMD vectorization and lightweight runtimes.
- **Interactive Standalone GUIs:** Every flagship ML system features an interactive zero-dependency HTML5/Tailwind/Canvas dashboard (`index.html`) for instant browser-based live verification.
- **Verified Championship Execution:** 1st Place Winner out of 44 university teams at IT Boot Camp 2026 for architecting the *TitikAman* emergency disaster mitigation platform.

---

## Technical Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=python,pytorch,fastapi,php,laravel,postgres,mysql,redis,docker,linux,git,ts,react,tailwind" alt="Core Technologies" />
</p>

- **Languages:** Python (Advanced Vectorization), SQL (PostgreSQL, MySQL), PHP, JavaScript/TypeScript, Go (Basic), Bash
- **Machine Learning & SciML:** Split Conformal Prediction, Causal ML (Meta-Learners, X-Learner, Doubly Robust CATE), LightGBM, Box Least Squares (BLS), Ragas Metrics, MLflow Tracking
- **Spatial & Streaming Systems:** Spearman Potential Pitch Control (PPCF), 4D NumPy Tensor Broadcasting, Concept Drift Monitoring (PSI, Wasserstein-1), Cost-Sensitive Decision Routing
- **Backend & Full-Stack:** FastAPI, Laravel 11/12, React 18, WebSockets (Laravel Reverb), RESTful APIs, Webhooks, PostGIS
- **Databases & Concurrency:** PostgreSQL, MySQL, Redis (Pub/Sub & Caching), Pessimistic Row Locking (`SELECT FOR UPDATE`), 3NF Modeling, Alembic
- **Testing & Quality Assurance:** Pytest, PHPUnit, k6 Load Testing, CI/CD GitHub Actions, Contract-First OpenAPI/Swagger Specs

---

## Flagship Machine Learning & Scientific Computing Engines

| System | Primary Novelty & Architecture | Benchmark & Latency | Automated Tests | Live UI |
| :--- | :--- | :--- | :---: | :---: |
| **[SpecRAG](https://github.com/Rangga11268/speculative-rag-engine)** | Shannon Entropy-Gated Speculative RAG, Okapi BM25 + NumPy SIMD Hybrid Search (RRF k=60), LRU Semantic Cache | **P50 Latency $-57.7\%$**, Compute $-72.2\%$, Cache $<1.0\text{ ms}$ | **288 Passed** | [`index.html`](https://github.com/Rangga11268/speculative-rag-engine) |
| **[Causal Uplift Engine](https://github.com/Rangga11268/causal-uplift-retention-engine)** | Heterogeneous Treatment Effects (CATE via X-Learner & DR-Learner) + Constrained Knapsack Budget Allocation | **Qini Gain $+18.68$**, Top Decile Lift $+42.0\%$, **Net ROI $+240.9\%$** | **13 Passed** | [`index.html`](https://github.com/Rangga11268/causal-uplift-retention-engine) |
| **[ExoTransit-Conformal](https://github.com/Rangga11268/exotransit-conformal-engine)** | NASA Kepler/TESS Exoplanet Transit Photometry, Vectorized Box Least Squares (BLS), Split Conformal Prediction | **$97.4\%$ Empirical Coverage** ($\ge 95\%$ nominal), **P99 $<7.10\text{ ms}$** | **18 Passed** | [`index.html`](https://github.com/Rangga11268/exotransit-conformal-engine) |
| **[GegenPress-PPCF](https://github.com/Rangga11268/gegenpress-ppcf-engine)** | Potential Pitch Control Field (Dr. William Spearman model) over 7,140 pitch cells via 4D NumPy Tensor Broadcasting | **$409.2\times$ Speedup** ($23.75\text{ ms}$/frame, **42.1 FPS** on CPU) | **29 Passed** | [`index.html`](https://github.com/Rangga11268/gegenpress-ppcf-engine) |
| **[StreamGuard](https://github.com/Rangga11268/streamguard-fraud-engine)** | Streaming Fraud under Delayed Feedback (1-4h vs 14-30d), Unsupervised Drift Monitoring (PSI/Wasserstein-1) | **Financial Loss $-40.33\%$**, **P99 Latency $1.19\text{ ms}$** | **174 Passed** | [`index.html`](https://github.com/Rangga11268/streamguard-fraud-engine) |

---

## Production Full-Stack & Distributed Web Systems

### 1. [TitikAman: Emergency Disaster Mitigation & Spatial Dispatch Platform](https://github.com/Rangga11268/titikAman)
> **1st Place Champion & HAKI Submission:** IT Boot Camp Software Development for Industry 2026 (Awarded by Faculty & Industry Panelists)
- Architected real-time WebSocket fleet dispatch engine via Laravel Reverb and Echo with distributed mutex locking, eliminating duplicate dispatches with $<150\text{ms}$ network latency.
- Optimized spatial queries on 50,000+ flood hazard coordinates via PostGIS GiST indexing and bounding-box pruning (`&&`), slashing p95 latency from $420\text{ms}$ to $38\text{ms}$ without sequential table scans.
- Maintained **0.00% error rate** under k6 load tests sustaining 500 Virtual Users @ 1,250 req/sec across 59 automated PHPUnit test suites on a 2 vCPU / 2GB RAM container.
- **Tech Stack:** Laravel 12, PHP 8.3, PostGIS, MySQL, WebSockets (Reverb), Leaflet.js, Tailwind CSS

### 2. [Makarya: Escrow-Backed Micro-Freelancing Ecosystem](https://github.com/Rangga11268/makarya)
> Full-stack freelancing platform connecting university talents with local businesses
- Engineered ACID-compliant escrow wallet with pessimistic row-level locking (`SELECT FOR UPDATE`) and idempotency keys, guaranteeing zero financial leakage across concurrent settlements.
- Implemented idempotent webhook pipeline with HMAC-SHA512 verification for Midtrans Payment Gateway, eliminating duplicate charges with sub-second status reconciliation.
- Structured 3NF relational schema across 15 tables with Alembic migrations, optimizing composite indexing and async SQLAlchemy sessions for $<25\text{ms}$ p95 latency.
- **Tech Stack:** Python, FastAPI, React 18, PostgreSQL, SQLAlchemy, Alembic, Tailwind CSS, Midtrans API

### 3. [ApaPesan: Real-Time Communication Platform](https://github.com/Rangga11268/ApaPesan-Laravel-project)
> High-frequency real-time messaging application pairing Laravel 11 backend with React / Inertia.js SPA
- Integrated Laravel Reverb WebSockets with optimistic UI updates; mitigated ghost socket memory leaks via 30s ping/pong heartbeats and exponential backoff client reconnects.
- Designed tiered Redis rate-limiting and automated health-check monitoring ensuring 99.9% uptime during high-frequency chat traffic.
- **Tech Stack:** Laravel 11, React 18, Inertia.js, WebSockets (Reverb), Redis, MySQL, Tailwind CSS

### 4. [SRB Motor V3: Automotive Dealership ERP & Inventory Portal](https://github.com/Rangga11268/SrbMotorV3)
> Dealership operational management platform for multi-tier vehicle parts inventory and financing
- Constructed full-stack ERP managing 1,000+ vehicle parts, installment financing calculations, and automated digital transactional invoices.
- Integrated Midtrans Snap payment gateway with automated callback reconciliation, cutting payment verification latency to instant ($<2\text{s}$).
- **Tech Stack:** Laravel 11, MySQL, Midtrans Snap, Fonnte WhatsApp API, Tailwind CSS

---

## Technical Writing & System Documentation

- **OpenAPI & Swagger Specifications:** Contract-first API specifications ensuring type-safe client integration without ambiguity.
- **Formal SDLC Artifacts:** Product Requirements Documents (PRD), entity-relationship models (3NF ERDs), architectural sequence flows, and comprehensive UAT testing plans.
- **Academic & HAKI Documentation:** Authored and defended the 89-page technical engineering documentation and user manual for TitikAman registered for national intellectual property rights (HAKI).

---

## GitHub Activity & Analytics

<div align="center">
  <img src="https://github-readme-stats-eight-theta.vercel.app/api?username=Rangga11268&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" alt="GitHub Stats" />
  <img src="https://github-readme-stats-eight-theta.vercel.app/api/top-langs/?username=Rangga11268&layout=compact&theme=tokyonight&hide_border=true" alt="Top Languages" />
</div>

---

<div align="center">
  <sub>Darell Rangga Putra Rachman · Software Engineering, Machine Learning & Systems Architecture</sub>
</div>
