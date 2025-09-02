# REST API Integration Plan

I’ve chosen **REST APIs** to integrate web services between client and server with standardized JSON, versioned interfaces, and predictable behavior.

---

## Integration Phases (Actionable)

###  Phase 1: **Contract-First Foundation**

Define a solid, reviewable API contract upfront—this minimizes misalignment and speeds future work.

- **Deliverables:**
  - `docs/openapi.yaml` describing initial endpoints (e.g., `GET /api/v1/customers/{id}/loan-summary`, `POST /api/v1/loan-applications`)
  - Include **operationId**, schemas, response examples.
  - Validate using an OpenAPI linter/editor.
- **Why:** A contract-first approach aligns all teams, supports parallel development, and prevents inconsistencies. Tools like Swagger, Postman, and linters provide early feedback. 
- **Scaffold:** Generate boilerplate (e.g., routes, controllers) from the spec to focus implementation on business logic. 

###  Phase 2: **Scaffold & Build Incrementally (Strangler Fig Pattern)**

Implement endpoints one slice at a time, allowing the legacy/incremental system to function continuously.

- **Steps:**
  - Create controllers, routes, and resource transformers following the contract.
  - Use a facade (API router) to direct calls either to legacy handlers or to new handlers.
  - Replace functionality slice-by-slice without disrupting production.
- **Why:** The Strangler Fig pattern reduces risk by migrating feature-by-feature rather than via a risky rewrite. 

###  Phase 3: **Validation, Testing & CI**

Ensure correctness, stability, and reproducibility across changes.

- **Deliverables:**
  - Write feature tests for each endpoint (success + failure paths, including DB asserts for POST).
  - Optionally, use OpenAPI validators to compare implementation vs. spec. 
  - Setup CI (e.g., GitHub Actions) to run tests and lint on pull requests.

###  Phase 4: **Document & Demonstrate**

Make your API easy to grasp, test, and use—from mock requests to implementation guidance.

- **Deliverables:**
  - `docs/learning/README.md` containing:
    - Sample `curl` commands (success and error cases)
    - Short instructions: “Read the spec → Run tests”
    - Link to `openapi.yaml`
  - Ensure the documentation reflects actual behavior and passes CI validation consistently.

---

## Integration Tasks (SMART, Dated)

| Task | Title                               | Start         | End           | Success Criteria                              | Proof Artifacts                                       | Branch                            |
|------|-------------------------------------|---------------|----------------|-----------------------------------------------|--------------------------------------------------------|-----------------------------------|
| 1    | Contract-First API Spec              | 2025-09-03    | 2025-09-05    | `openapi.yaml` exists and validates locally     | Linter output, spec file in repo, brief doc snippet   | `spec/INIT`                       |
| 2    | Scaffold Controllers & Routes        | 2025-09-06    | 2025-09-08    | Controllers, transformers and routes implemented | Basic curl sample in README, scaffold code committed  | `scaffold/api-endpoints`          |
| 3    | Implement GET Loan Summary           | 2025-09-09    | 2025-09-11    | GET works; expected JSON returned; 404 path covered | Passing feature tests, curl example in README        | `feature/get-loan-summary`        |
| 4    | Implement POST Loan Application      | 2025-09-12    | 2025-09-14    | POST validates and creates record; 422 on validation errors | Tests green, request/response examples logged      | `feature/post-loan-application`   |
| 5    | CI & Regression Testing              | 2025-09-15    | 2025-09-17    | CI green; regression suite passing               | Screenshot of CI status; test reports in `test-reports/` | `chore/ci-and-tests`              |
| 6    | Final Documentation                  | 2025-09-18    | 2025-09-20    | README includes examples + links + “how to test” | README updated with examples, CI badge                | `docs/finalize`                   |

---

## Endpoint Sketches

```http
GET /api/v1/customers/{id}/loan-summary
200 OK
{
  "customer_id": 123,
  "loan": { … }
}
POST /api/v1/loan-applications
201 Created
{ … }
