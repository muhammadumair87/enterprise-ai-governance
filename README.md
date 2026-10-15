# Enterprise AI Usage, Licence & Cost Governance

A privacy-safe enterprise AI governance prototype for monitoring AI tool usage, licence utilisation, token consumption, departmental capacity and cost.

The project demonstrates how an AI Enablement or R&D Operations function could combine deterministic governance logic with AI-assisted analysis to support better operational decisions across an enterprise AI tool estate.

> **Portfolio Project 1 — Enterprise AI Operations & Governance**

---

## Overview

As organisations expand the use of tools such as GitHub Copilot, Cursor, ChatGPT Enterprise and other AI platforms, AI Enablement teams need visibility beyond simple licence counts.

Operational questions quickly emerge:

- Which licences are actively being used?
- Which licences appear underutilised?
- Which departments are approaching their usage limits?
- Where is capacity significantly underutilised?
- Are current budgets sufficient?
- What may happen before the end of the reporting period?
- Can existing capacity be optimised before additional spend is approved?
- Which situations require investigation rather than automated action?

This prototype explores those questions through a lightweight governance and reporting layer.

---

## Core Capabilities

### Licence Governance

The system analyses licence activity and identifies accounts that may require review.

Examples include:

- prolonged inactivity
- potentially underutilised licences
- unusually low activity
- opportunities for licence reassignment
- estimated potential savings

Inactivity is deliberately treated as a **review trigger rather than proof that a licence should be removed**.

Business context and human validation remain necessary before entitlement changes are made.

---

### Usage & Token Monitoring

The prototype evaluates AI consumption using signals such as:

- input tokens
- output tokens
- cached tokens
- uncached tokens
- request volume
- usage allocation
- estimated spend

This provides a foundation for identifying both high-utilisation and low-utilisation patterns.

---

### Department-Level Governance

Usage is evaluated at department level rather than only at individual-user level.

Example governance areas include:

- Engineering
- IT
- HR
- Finance
- Marketing

Department configuration can define:

- token allocation
- monthly budget
- warning threshold
- critical threshold

This separates governance policy from the analysis logic and allows operational thresholds to be changed without rewriting the application.

---

## Forecasting

The prototype includes a transparent usage forecast to estimate potential end-of-period consumption.

The goal is not to claim sophisticated machine-learning forecasting.

Instead, the prototype deliberately uses understandable forecasting logic to demonstrate how an AI Enablement team could identify capacity risks before users are interrupted.

For example:

```text
Current utilisation
        ↓
Projected month-end utilisation
        ↓
Threshold comparison
        ↓
Monitor / Capacity Risk / Likely Limit Breach
```

A production implementation could extend this using historical consumption, seasonality, workload patterns and vendor telemetry.

---

## Cost & FinOps Analysis

The governance layer considers both utilisation and financial impact.

It can identify situations such as:

- departments approaching monthly budgets
- departments approaching usage limits
- potentially oversized allocations
- potential licence savings
- abnormal usage patterns
- possible capacity pressure

Importantly, high consumption does not automatically result in a recommendation to purchase more capacity.

The system encourages validation of demand and existing capacity before additional spend.

---

## Capacity Optimisation Concept

A key governance principle is:

> **Optimise existing enterprise AI capacity before automatically increasing spend.**

For example, imagine IT is consuming AI capacity rapidly while Finance or HR is forecast to leave a significant allocation unused.

A governance workflow could evaluate whether unused capacity may safely be reassigned, where technically and contractually supported.

Any such recommendation should consider:

- forecast demand
- business criticality
- remaining-period workload
- safety buffers
- seasonality
- platform capabilities
- contractual constraints
- human approval

This project provides the operational visibility required for such decisions.

The decision-orchestration layer is explored further in **Portfolio Project 2 — Enterprise AI Enablement Multi-Agent System**.

---

## Anomaly Detection

The prototype also looks for combinations of signals that deserve investigation.

For example:

```text
High token consumption
+
Long period since recorded user activity
=
Potential data-quality, automation or usage anomaly
```

An anomaly is not automatically classified as misuse.

Possible explanations may include:

- automation
- service accounts
- inaccurate activity reporting
- shared workloads
- unusual project activity
- data-quality issues

The appropriate response is investigation rather than automatic enforcement.

---

## AI-Assisted Management Recommendations

After deterministic metrics are calculated, the project can use an OpenAI API integration to generate a management-oriented governance summary.

The AI layer receives calculated operational signals and converts them into recommendations concerning:

- licence reviews
- cost pressure
- capacity risks
- utilisation anomalies
- monitoring priorities
- potential optimisation opportunities

The AI model is used for **interpretation and decision support**, not as the source of truth for deterministic calculations.

---

## Design Principle: Deterministic Logic vs AI Reasoning

A core architectural principle across this portfolio is:

> **Use deterministic software for calculations and LLMs for interpretation.**

Examples of deterministic logic include:

- utilisation percentages
- token totals
- threshold comparisons
- budget calculations
- licence inactivity periods
- forecasts
- potential savings calculations

AI reasoning can then help interpret those signals and produce management-oriented recommendations.

This separation reduces the risk of relying on an LLM to invent or inconsistently calculate operational metrics.

---

## Architecture

```text
Synthetic Enterprise AI Usage Data
                │
                ▼
        CSV / Data Ingestion
                │
                ▼
      Governance Configuration
                │
                ▼
     Deterministic Python Engine
                │
       ┌────────┼─────────┐
       ▼        ▼         ▼
    Licence    Usage     Cost
    Analysis  Analysis   Analysis
       │        │         │
       └────────┼─────────┘
                ▼
             Forecast
                │
                ▼
        Anomaly Detection
                │
                ▼
       OpenAI API Analysis
                │
                ▼
     Management Recommendation
                │
                ▼
        Governance Reports
```

---

## Example Data Model

The demonstration dataset can contain fields such as:

```text
name
department
tool
days_since_activity
licence_cost_eur
input_tokens
output_tokens
cached_tokens
uncached_tokens
request_count
usage_limit
estimated_spend_eur
```

Example AI platforms represented in synthetic scenarios may include:

- GitHub Copilot
- Cursor
- ChatGPT
- other enterprise AI services

---

## Example Governance Scenario

Consider the following simplified situation:

```text
IT
High utilisation
Forecast capacity pressure

HR / Finance
Low utilisation
Forecast unused capacity
```

The appropriate enterprise response should not simply be:

```text
IT usage high → buy more capacity
```

Instead:

```text
Detect capacity pressure
        ↓
Validate forecast
        ↓
Review existing allocations
        ↓
Identify safely unused capacity
        ↓
Validate business requirements
        ↓
Consider reallocation where supported
        ↓
Human approval
        ↓
Monitor outcome
```

This demonstrates the difference between basic usage reporting and operational AI governance.

---

## Privacy-Safe Demonstration

All business and user information used by this repository is **synthetic demonstration data**.

No confidential employer, customer or production usage data is required to demonstrate the architecture.

Synthetic data allows realistic enterprise scenarios to be modelled while maintaining privacy and confidentiality.

The production integration pattern would remain similar:

```text
Vendor APIs
Identity / HR Systems
Usage APIs
Billing APIs
        │
        ▼
Normalisation Layer
        │
        ▼
Governance Engine
        │
        ▼
Reporting / Decision Support
```

---

## Production Architecture

A production implementation could replace the demonstration CSV dataset with approved enterprise data sources.

Potential integrations include:

- AI vendor usage APIs
- licence-management APIs
- identity providers
- SSO / SCIM
- HR lifecycle systems
- billing systems
- security telemetry
- data warehouse / BI platforms

Additional production controls would include:

- API authentication
- secrets management
- role-based access control
- pagination
- rate-limit handling
- retry/backoff
- reconciliation
- logging
- alerting
- approval workflows
- monitoring
- audit trails

---

## Human-in-the-Loop Governance

This prototype intentionally avoids automatically performing high-impact administrative actions.

For example, the system may recommend reviewing:

- an inactive licence
- a departmental capacity allocation
- an unusual usage pattern
- additional AI spend

But the recommendation does not itself constitute approval.

This follows the principle:

```text
Detect
  ↓
Analyse
  ↓
Recommend
  ↓
Human Review
  ↓
Approved Action
  ↓
Audit
```

---

## Project Structure

A typical project structure is:

```text
Enterprise AI Usage, Licence & Cost Governance/
│
├── config/
│   └── department_limits.csv
│
├── data/
│   └── demo_usage.csv
│
├── reports/
│
├── license_audit.py
├── test_openai_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

Generated report filenames may vary by timestamp.

---

## Running the Prototype

Create and activate a Python virtual environment.

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Configure the OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

Do not store API credentials directly in source code or commit them to Git.

Run the governance analysis:

```bash
python3 license_audit.py
```

---

## Security

Secrets should be provided through environment variables or an approved secrets-management platform.

The repository should never contain:

- production API keys
- passwords
- access tokens
- confidential customer information
- proprietary company datasets

The included demonstration data is intended to be synthetic.

---

## Limitations

This repository is an enterprise **prototype**, not a production governance platform.

Current limitations may include:

- synthetic rather than live enterprise telemetry
- simplified forecasting
- limited historical trend analysis
- no automatic vendor provisioning
- no automatic licence removal
- no automatic capacity transfer
- limited alerting/integration capabilities
- human approval remains external to the prototype

These constraints are intentional and keep the project focused on demonstrating architecture and governance principles.

---

## Production Roadmap

Potential future extensions include:

1. Vendor API integrations
2. Identity and SCIM integration
3. Historical usage storage
4. Advanced forecasting
5. Automated threshold alerts
6. Teams / Slack notifications
7. Approval workflows
8. BI dashboards
9. Policy-as-code governance
10. Enterprise audit logging
11. Multi-vendor cost normalisation
12. Automated reconciliation

---

## Related Project

### Enterprise AI Enablement Multi-Agent System

The second portfolio project builds on these operational governance concepts by introducing specialist AI agents for:

- licence governance
- AI FinOps
- security assessment
- adoption analysis
- capacity optimisation
- governance decision support
- auditable recommendations

The relationship between the projects can be summarised as:

```text
Project 1
Observe → Measure → Forecast → Detect
                    │
                    ▼
Project 2
Route → Analyse → Optimise → Govern → Audit
```

Together, the projects explore how an Enterprise AI Enablement function could combine operational visibility, deterministic controls, AI-assisted reasoning and human governance.

---

## Purpose

This project was built as a hands-on exploration of enterprise AI enablement, with particular focus on the intersection of:

- AI platform operations
- SaaS administration
- licence management
- FinOps
- security
- governance
- developer enablement
- automation
- responsible AI adoption

The objective is not to replace human operational ownership with AI.

The objective is to demonstrate how automation and AI-assisted analysis can help enterprise teams make **better-informed, measurable and auditable decisions**.
