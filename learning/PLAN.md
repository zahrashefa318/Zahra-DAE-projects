# REST API Integration Plan

I’ve chosen **REST APIs** for my project to integrate web services between the client and server in a clean, standardized way. REST emphasizes clear resource naming, stateless requests, and predictable use of HTTP methods (GET, POST, PUT/PATCH, DELETE), which improves consistency and interoperability across the system.  

> Why REST?
> - Predictable resource design and versioning
> - Uniform JSON structures for request/response
> - Easier testing and automation across services

---

## Integration Approach

1. **Learn Deeply**
   - Review REST fundamentals (statelessness, uniform interface, resource modeling, HTTP methods and status codes).
   - Study API design guidance and conventions (nouns for resources, pagination, filtering, error formats, versioning, auth).  
   _References: Microsoft REST API design guidance; OpenAPI best practices; Swagger/Stack Overflow design tips.

2. **Incremental Modernization**
   - Apply REST endpoints where they add the most value first, keeping legacy UI flows running while introducing an API layer.
   - Use a “**strangler**” approach: route only selected features through the new API and expand coverage over time.  
   _References: Strangler Fig modernization pattern (Fowler, Azure Architecture Center).

3. **Test, Compare, Prove**
   - Add unit/integration tests for each endpoint; automate in CI.
   - Capture **before vs. after** behavior (manual cURL examples + screenshots of passing CI).

**Specific capability added:** standard, structured data transmission (primarily JSON) and consistent API contracts that are easy to document and test.  
_See also: REST/HTTP method guidance and design checklists._ 

---

## Standards & Conventions (Project-Wide)

- **Content type:** `application/json`
- **Naming:** plural nouns for collections (`/api/customers`, `/api/loan-applications`)
- **Versioning:** prefix routes with `/api/v1/...`
- **Errors:** JSON problem details with `code`, `message`, `details`
- **Auth (future):** token-based (e.g., JWT) with `Authorization: Bearer <token>`
- **Docs:** OpenAPI spec stored at `docs/openapi.yaml` and rendered in README  
_Reference: Microsoft REST API design guidance & OpenAPI best practices._ 

---

## SMART Framing

Each task below is **Specific, Measurable, Achievable, Relevant, Time-bound** (SMART) with explicit success criteria and proof capture. 

---

## My Three Integration Tasks (small, testable, dated)

> **Note:** Replace dates if you need different targets. Today is **2025-09-02**.

### Task 1 — Title: **GET Loan Summary for a Customer**

- **Description:** Implement `GET /api/v1/customers/{id}/loan-summary` to return a summarized JSON of the customer’s approved loan account (principal, interest rate, term, start/end dates, current status).
- **Start date:** 2025-09-03  
- **Target completion date:** 2025-09-05  
- **Success criterion (explicit):** An integration test confirms the endpoint returns the expected JSON shape and values for seeded sample data; returns `404` for a non-existent customer; returns `403/401` when auth guard (stubbed for now) fails.
- **Proof method:**  
  1) Screenshot of passing CI run for the new integration test.  
  2) Paste a `curl` request/response example into `docs/learning/README.md`.  
  3) Add the endpoint to `docs/openapi.yaml` and include a short snippet in the README.
- **Where I will start Task 1:** `feature/get-loan-summary-endpoint`

### Task 2 — Title: **POST Create Loan Application**

- **Description:** Implement `POST /api/v1/loan-applications` to create a new loan application with validated JSON (`customer_id`, `requested_amount`, `terms_months`, `purpose`). On success, return `201` with the created resource and Location header; on validation failure, return `422` with errors.
- **Start date:** 2025-09-06  
- **Target completion date:** 2025-09-08  
- **Success criterion (explicit):** Integration test demonstrates:  
  - valid payload → `201` and persisted record  
  - invalid payload → `422` with field-level error messages  
  - OpenAPI schema is updated and matches responses
- **Proof method:**  
  1) CI screenshot with green tests.  
  2) `curl` example (request + response) saved in `docs/learning/README.md`.  
  3) Database assertion screen or console log from test run (sanitized).
- **Where I will start Task 2:** `feature/post-loan-application`

### Task 3 — Title: **Automated Regression Tests for Loan Endpoints**

- **Description:** Add regression tests covering both new endpoints to ensure changes don’t break API contracts (status codes, JSON schema, pagination/errors where applicable).
- **Start date:** 2025-09-09  
- **Target completion date:** 2025-09-11  
- **Success criterion (explicit):** All regression tests pass in CI; JSON schema validation is enforced for success/error responses; README links to a test report.
- **Proof method:**  
  1) CI screenshot with the regression suite green.  
  2) Store HTML/JSON test reports under `test-reports/` and link from README.  
  3) Include a short “How to run tests” section in `README.md`.
- **Where I will start Task 3:** `chore/api-regression-tests`

---

## Quick Overview

| Task | Title                                       | Start       | Target End  | Success (summary)                                        | Proof artifacts                                             |
|------|---------------------------------------------|-------------|-------------|-----------------------------------------------------------|-------------------------------------------------------------|
| 1    | GET Loan Summary for a Customer             | 2025-09-03  | 2025-09-05  | GET returns expected JSON; 404/401/403 paths correct      | CI screenshot; curl sample in README; OpenAPI updated       |
| 2    | POST Create Loan Application                | 2025-09-06  | 2025-09-08  | 201 on valid; 422 on invalid; schema documented           | CI screenshot; curl sample; DB assertion proof              |
| 3    | Automated Regression Tests for Endpoints    | 2025-09-09  | 2025-09-11  | Regression suite passes; schema checks enforced           | CI screenshot; saved test reports; README run instructions  |

---

## Endpoint Sketches (for reference)

```http
GET /api/v1/customers/{id}/loan-summary
Accept: application/json

200 OK
{
  "customer_id": 123,
  "loan": {
    "loan_id": 456,
    "principal": 10000.00,
    "interest_rate": 0.08,
    "terms_months": 24,
    "start_date": "2025-06-01",
    "end_date": "2027-05-31",
    "status": "approved"
  }
}

POST /api/v1/loan-applications
Content-Type: application/json
Accept: application/json

{
  "customer_id": 123,
  "requested_amount": 10000.00,
  "terms_months": 24,
  "purpose": "Small business working capital"
}

201 Created
Location: /api/v1/loan-applications/789
{
  "application_id": 789,
  "customer_id": 123,
  "requested_amount": 10000.00,
  "terms_months": 24,
  "purpose": "Small business working capital",
  "status": "submitted",
  "created_at": "2025-09-06T12:34:56Z"
}
