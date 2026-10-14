# Enterprise AI Usage, Licence & Cost Governance

A privacy-safe enterprise AI governance prototype for monitoring AI-tool usage, licence utilisation, token consumption, departmental budgets, capacity forecasts, governance anomalies and AI-assisted management recommendations.

The project demonstrates how an AI Enablement or R&D Operations team could combine deterministic governance rules with an LLM-based interpretation layer.

> This repository uses synthetic demonstration data. No confidential employee, company, customer or production usage data is included.

---

## Overview

Enterprise AI platforms can create operational challenges around:

- licence utilisation
- unused or inactive accounts
- token and request consumption
- departmental AI budgets
- unexpected usage patterns
- capacity planning
- cost forecasting
- governance reviews

This prototype provides a lightweight governance layer that analyses usage and licence data, applies configurable policies, forecasts department-level utilisation and generates management-ready recommendations through the OpenAI API.

---

## Architecture

```text
Synthetic Usage Data
data/demo_usage.csv
        |
        v
+----------------------------+
| Python Governance Engine   |
| license_audit.py           |
+----------------------------+
        ^
        |
Department Governance Policy
config/department_limits.csv

        |
        v

+----------------------------+
| Licence Governance         |
| Usage Monitoring           |
| Cost Analysis              |
| Anomaly Detection          |
| Department Forecasting     |
+----------------------------+

        |
        v
OpenAI API
        |
        v
Management Recommendation
        |
        v
reports/