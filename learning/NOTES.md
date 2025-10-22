# Observability & Logging: Project Notes

This document tracks your progress and implementation of observability features in your backend or cybersecurity project. You will update this continuously as you build health checks, logs, and metrics.

---

## 1. Health Check Endpoint

**Have you implemented a health-check endpoint?**  
(Replace `[ ]` with `[x]`)

-   [1 ] Yes
-   [ ] No
-   [ ] Not applicable to my project

**Your endpoint path:**  
/api/health

```
# Actual output example:
{
  "status": "ok",
  "version": "9.52.20"
}

```

**Why is this useful?**  
Allows load balancers and orchestrators to verify the service is alive and route traffic only to healthy instances (e.g., Kubernetes liveness/readiness probes; AWS ALB target health checks).
Allows external systems to check if the service is running and responsive without accessing internal logic.

---

## 2. Health Check Test

**Did you write a test for the health-check endpoint?**

-   [1] Yes
-   [ ] No

**Paste your test code or description here:**

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class HealthTest extends TestCase
{
    /** @test */
    public function health_endpoint_returns_ok()
    {
        $this->getJson('/api/health')
             ->assertOk()
             ->assertJson(['status' => 'ok']);
    }
}

```

---

## 3. Log Event or Metric

**Name of log event or metric:**  
Example: `"user_login_success"`, `"unauthorized_attempt"`, `"system_heartbeat"`

**What triggers this?**  
Example: Each time a user logs in, or every 5 minutes for uptime tracking.

**Sample output format or log:**

```
# Example (JSON log)
{
  "event": "unauthorized_attempt",
  "ip": "192.168.1.101",
  "timestamp": "2025-09-15T14:31:24Z"
}
```

**Where is this implemented in your code?**  
app/Http/Controllers/Api/LoanOfficerController.php → customerdestroy()
app/Services/LoanOfficerService.php → deleteCustomer() (transaction; catch/propagate errors)

---

## 4. Optional Monitoring Toolsa

Only fill this out if you added any external monitoring.

**Did you use monitoring tools (e.g. Grafana, Prometheus, Kibana)?**

-   [ ] Yes
-   [1] No

**Tool name(s):**  
N/A

**Screenshot or description of what the tool shows:**
N/A

```
# Example description:
Dashboard displays request count, error rate, and memory usage over time.
```

---

## 5. Reflection & Learning

**What did you learn while implementing observability in your project?**

> Example: I learned that structured logging helps track real user activity and makes error detection easier.

**Anything you would do differently or improve in the future?**

> Example: I would log more internal actions, like database queries and job status.

---
