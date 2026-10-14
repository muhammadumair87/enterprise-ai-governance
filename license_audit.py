import csv
import os
from datetime import datetime
from collections import defaultdict

from openai import OpenAI


# ============================================================
# ENTERPRISE AI USAGE, LICENCE & COST GOVERNANCE
#
# Demo architecture:
#
# data/demo_usage.csv
#        ↓
# license_audit.py
#        ↑
# config/department_limits.csv
#        ↓
# Usage / Licence / Cost / Forecast / Anomaly Analysis
#        ↓
# OpenAI API Management Recommendation
#        ↓
# reports/
#
# IMPORTANT:
# The dataset used by this prototype is synthetic demo data.
# ============================================================


# ============================================================
# 1. FILE LOCATIONS
# ============================================================

DATA_FILE = "data/demo_usage.csv"
CONFIG_FILE = "config/department_limits.csv"
REPORTS_DIR = "reports"

os.makedirs(REPORTS_DIR, exist_ok=True)


# ============================================================
# 2. LOAD SYNTHETIC USAGE DATA
# ============================================================

users = []

with open(DATA_FILE, "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        user = {
            "name": row["name"],
            "department": row["department"],
            "tool": row["tool"],

            "days_since_activity": int(
                row["days_since_activity"]
            ),

            "licence_cost_eur": float(
                row["licence_cost_eur"]
            ),

            "input_tokens": int(
                row["input_tokens"]
            ),

            "output_tokens": int(
                row["output_tokens"]
            ),

            "cached_tokens": int(
                row["cached_tokens"]
            ),

            "uncached_tokens": int(
                row["uncached_tokens"]
            ),

            "request_count": int(
                row["request_count"]
            ),

            "user_token_limit": int(
                row["user_token_limit"]
            ),

            "estimated_spend_eur": float(
                row["estimated_spend_eur"]
            )
        }

        # Calculate total token activity
        user["total_tokens"] = (
            user["input_tokens"]
            + user["output_tokens"]
        )

        # Calculate individual user utilisation
        if user["user_token_limit"] > 0:

            user["usage_percentage"] = round(
                (
                    user["total_tokens"]
                    / user["user_token_limit"]
                ) * 100,
                1
            )

        else:

            user["usage_percentage"] = 0

        users.append(user)


# ============================================================
# 3. LOAD DEPARTMENT GOVERNANCE CONFIGURATION
# ============================================================

department_config = {}

with open(CONFIG_FILE, "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        department_config[row["department"]] = {

            "token_limit": int(
                row["token_limit"]
            ),

            "monthly_budget_eur": float(
                row["monthly_budget_eur"]
            ),

            "warning_threshold_percent": float(
                row["warning_threshold_percent"]
            ),

            "critical_threshold_percent": float(
                row["critical_threshold_percent"]
            )
        }


# ============================================================
# 4. LICENCE REVIEW
# ============================================================

# Inactivity is a REVIEW trigger.
# It does NOT automatically remove a licence.

LICENCE_REVIEW_DAYS = 30

for user in users:

    user["licence_review"] = (
        user["days_since_activity"]
        > LICENCE_REVIEW_DAYS
    )

    if user["licence_review"]:

        user["potential_savings_eur"] = (
            user["licence_cost_eur"]
        )

    else:

        user["potential_savings_eur"] = 0


# ============================================================
# 5. USER USAGE STATUS
# ============================================================

for user in users:

    usage = user["usage_percentage"]

    if usage >= 100:

        user["usage_status"] = (
            "Critical - limit reached/exceeded"
        )

    elif usage >= 80:

        user["usage_status"] = (
            "Warning - high usage"
        )

    elif usage < 20:

        user["usage_status"] = (
            "Low usage"
        )

    else:

        user["usage_status"] = (
            "Normal"
        )


# ============================================================
# 6. DETECT USER-LEVEL ANOMALIES
# ============================================================

for user in users:

    anomalies = []

    # High token usage but long period since recorded activity
    if (
        user["days_since_activity"] > 30
        and user["usage_percentage"] >= 70
    ):

        anomalies.append(
            "High token usage despite low recorded activity"
        )

    # Low usage combined with an inactive licence
    if (
        user["days_since_activity"] > 30
        and user["usage_percentage"] < 20
    ):

        anomalies.append(
            "Low usage combined with inactive licence"
        )

    if anomalies:

        user["anomaly"] = "; ".join(anomalies)

    else:

        user["anomaly"] = "None"


# ============================================================
# 7. BUILD DEPARTMENT AGGREGATES
# ============================================================

department_data = defaultdict(
    lambda: {
        "users": 0,
        "tokens_used": 0,
        "requests": 0,
        "current_spend_eur": 0,
        "licence_cost_eur": 0,
        "potential_savings_eur": 0
    }
)

for user in users:

    department = user["department"]

    department_data[department]["users"] += 1

    department_data[department]["tokens_used"] += (
        user["total_tokens"]
    )

    department_data[department]["requests"] += (
        user["request_count"]
    )

    department_data[department][
        "current_spend_eur"
    ] += user["estimated_spend_eur"]

    department_data[department][
        "licence_cost_eur"
    ] += user["licence_cost_eur"]

    department_data[department][
        "potential_savings_eur"
    ] += user["potential_savings_eur"]


# ============================================================
# 8. DEPARTMENT UTILISATION + FORECASTING
# ============================================================

# Simple transparent demo forecast:
# project current usage/spend by 20%.
#
# This is NOT an ML forecast.
# It is deliberately simple for explainability.

FORECAST_GROWTH_FACTOR = 1.20


for department, values in department_data.items():

    if department not in department_config:

        raise ValueError(
            f"No configuration found for department: "
            f"{department}"
        )

    config = department_config[department]

    token_limit = config["token_limit"]
    monthly_budget = config["monthly_budget_eur"]

    warning_threshold = (
        config["warning_threshold_percent"]
    )

    critical_threshold = (
        config["critical_threshold_percent"]
    )


    # --------------------------------------------------------
    # Current token utilisation
    # --------------------------------------------------------

    if token_limit > 0:

        current_usage_percentage = (
            values["tokens_used"]
            / token_limit
        ) * 100

    else:

        current_usage_percentage = 0


    values["token_limit"] = token_limit

    values["monthly_budget_eur"] = (
        monthly_budget
    )

    values["warning_threshold_percent"] = (
        warning_threshold
    )

    values["critical_threshold_percent"] = (
        critical_threshold
    )

    values["current_usage_percentage"] = round(
        current_usage_percentage,
        1
    )


    # --------------------------------------------------------
    # Forecast token consumption
    # --------------------------------------------------------

    forecast_tokens = round(
        values["tokens_used"]
        * FORECAST_GROWTH_FACTOR
    )

    values["forecast_tokens"] = (
        forecast_tokens
    )


    if token_limit > 0:

        forecast_usage_percentage = (
            forecast_tokens
            / token_limit
        ) * 100

    else:

        forecast_usage_percentage = 0


    values["forecast_usage_percentage"] = round(
        forecast_usage_percentage,
        1
    )


    # --------------------------------------------------------
    # Forecast spend
    # --------------------------------------------------------

    forecast_spend = (
        values["current_spend_eur"]
        * FORECAST_GROWTH_FACTOR
    )

    values["forecast_spend_eur"] = round(
        forecast_spend,
        2
    )


    if monthly_budget > 0:

        forecast_budget_percentage = (
            forecast_spend
            / monthly_budget
        ) * 100

    else:

        forecast_budget_percentage = 0


    values["forecast_budget_percentage"] = round(
        forecast_budget_percentage,
        1
    )


    # --------------------------------------------------------
    # CONFIG-DRIVEN FORECAST STATUS
    # --------------------------------------------------------

    forecast_usage = (
        values["forecast_usage_percentage"]
    )


    if forecast_usage >= critical_threshold + 10:

        values["forecast_status"] = (
            "Likely to exceed limit"
        )

        values["management_implication"] = (
            "Review workload and consider increased "
            "capacity only if business demand is justified."
        )


    elif forecast_usage >= critical_threshold:

        values["forecast_status"] = (
            "Capacity risk"
        )

        values["management_implication"] = (
            "Forecast is at or above the configured "
            "critical threshold; review allocation "
            "and budget before month-end."
        )


    elif forecast_usage >= warning_threshold:

        values["forecast_status"] = (
            "Monitor"
        )

        values["management_implication"] = (
            "Configured warning threshold reached; "
            "monitor usage before increasing capacity."
        )


    elif forecast_usage < 30:

        values["forecast_status"] = (
            "Underutilised"
        )

        values["management_implication"] = (
            "Review whether allocation or capacity "
            "is oversized."
        )


    else:

        values["forecast_status"] = (
            "Healthy"
        )

        values["management_implication"] = (
            "Current capacity appears appropriate."
        )


# ============================================================
# 9. GLOBAL GOVERNANCE METRICS
# ============================================================

total_users = len(users)

review_users = [
    user
    for user in users
    if user["licence_review"]
]

review_count = len(review_users)


potential_monthly_savings = sum(
    user["potential_savings_eur"]
    for user in users
)

potential_annual_savings = (
    potential_monthly_savings * 12
)

total_tokens = sum(
    user["total_tokens"]
    for user in users
)

total_requests = sum(
    user["request_count"]
    for user in users
)

total_ai_spend = sum(
    user["estimated_spend_eur"]
    for user in users
)


# ============================================================
# 10. TERMINAL SUMMARY
# ============================================================

print()
print(
    "ENTERPRISE AI USAGE, LICENCE & COST GOVERNANCE"
)
print("=" * 55)

print(
    f"Users analysed: {total_users}"
)

print(
    f"Users requiring licence review: "
    f"{review_count}"
)

print(
    f"Total tokens analysed: "
    f"{total_tokens:,}"
)

print(
    f"Total API requests: "
    f"{total_requests:,}"
)

print(
    f"Estimated AI spend: "
    f"EUR {total_ai_spend:.2f}"
)

print(
    f"Potential monthly licence savings: "
    f"EUR {potential_monthly_savings:.2f}"
)

print(
    f"Potential annual licence savings: "
    f"EUR {potential_annual_savings:.2f}"
)


# ============================================================
# 11. USER GOVERNANCE VIEW
# ============================================================

print()
print("USER GOVERNANCE")
print("-" * 55)

for user in users:

    review_text = (
        "REVIEW"
        if user["licence_review"]
        else "OK"
    )

    print(
        f"{user['name']} | "
        f"{user['department']} | "
        f"{user['tool']} | "
        f"{user['total_tokens']:,} tokens | "
        f"{user['usage_percentage']}% | "
        f"{user['usage_status']} | "
        f"Licence: {review_text}"
    )


# ============================================================
# 12. DEPARTMENT FORECAST VIEW
# ============================================================

print()
print("DEPARTMENT FORECAST")
print("-" * 55)

for department, values in department_data.items():

    print(
        f"{department} | "
        f"Current: "
        f"{values['current_usage_percentage']}% | "
        f"Forecast: "
        f"{values['forecast_usage_percentage']}% | "
        f"Thresholds: "
        f"{values['warning_threshold_percent']}%/"
        f"{values['critical_threshold_percent']}% | "
        f"Forecast spend: "
        f"EUR {values['forecast_spend_eur']:.2f} | "
        f"Status: "
        f"{values['forecast_status']}"
    )


# ============================================================
# 13. BUILD OPENAI MANAGEMENT CONTEXT
# ============================================================

user_context_lines = []

for user in users:

    user_context_lines.append(
        (
            f"- {user['name']} | "
            f"Department: {user['department']} | "
            f"Tool: {user['tool']} | "
            f"Days since activity: "
            f"{user['days_since_activity']} | "
            f"Tokens: {user['total_tokens']} | "
            f"Usage: {user['usage_percentage']}% | "
            f"Requests: {user['request_count']} | "
            f"AI spend: EUR "
            f"{user['estimated_spend_eur']:.2f} | "
            f"Licence cost: EUR "
            f"{user['licence_cost_eur']:.2f} | "
            f"Licence review: "
            f"{user['licence_review']} | "
            f"Anomaly: {user['anomaly']}"
        )
    )


department_context_lines = []

for department, values in department_data.items():

    department_context_lines.append(
        (
            f"- {department} | "
            f"Users: {values['users']} | "
            f"Tokens: {values['tokens_used']} | "
            f"Token limit: "
            f"{values['token_limit']} | "
            f"Current usage: "
            f"{values['current_usage_percentage']}% | "
            f"Forecast usage: "
            f"{values['forecast_usage_percentage']}% | "
            f"Warning threshold: "
            f"{values['warning_threshold_percent']}% | "
            f"Critical threshold: "
            f"{values['critical_threshold_percent']}% | "
            f"Current spend: EUR "
            f"{values['current_spend_eur']:.2f} | "
            f"Forecast spend: EUR "
            f"{values['forecast_spend_eur']:.2f} | "
            f"Budget: EUR "
            f"{values['monthly_budget_eur']:.2f} | "
            f"Status: "
            f"{values['forecast_status']}"
        )
    )


user_context = "\n".join(
    user_context_lines
)

department_context = "\n".join(
    department_context_lines
)


# ============================================================
# 14. OPENAI MANAGEMENT RECOMMENDATION
# ============================================================

print()
print(
    "Generating AI governance recommendation..."
)


client = OpenAI()


prompt = f"""
You are an enterprise AI enablement and governance analyst.

Analyse the following SYNTHETIC demonstration data.

The objective is to support enterprise AI operations across:
- licence governance
- usage monitoring
- token capacity
- cost governance
- anomaly investigation
- department forecasting

Do not recommend automatic licence removal solely because
a user is inactive or has low usage.

Treat inactivity and unusual usage as review triggers.

Forecasts are simple linear projections based on current
usage and are not machine-learning forecasts.

Potential savings are estimates and require validation.

GLOBAL METRICS

Users analysed: {total_users}
Licence reviews: {review_count}
Total tokens: {total_tokens}
Total requests: {total_requests}
Estimated AI spend: EUR {total_ai_spend:.2f}
Potential monthly licence savings:
EUR {potential_monthly_savings:.2f}

USER DATA

{user_context}

DEPARTMENT DATA

{department_context}

Produce a concise management report with exactly these sections:

1. Executive summary
2. Licence governance
3. Usage and token capacity
4. Department forecast
5. Budget risks
6. Anomalies requiring investigation
7. Recommended actions

Clearly distinguish between:
- confirmed observations
- forecasts
- potential savings
- recommendations

Do not claim that synthetic data represents real company data.
"""


try:

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    ai_recommendation = (
        response.output_text
    )

except Exception as error:

    ai_recommendation = (
        "OpenAI recommendation could not be generated.\n"
        f"Error: {error}"
    )


print()
print(ai_recommendation)


# ============================================================
# 15. CREATE TIMESTAMP
# ============================================================

timestamp = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)


# ============================================================
# 16. EXPORT DETAILED GOVERNANCE REPORT
# ============================================================

governance_filename = os.path.join(
    REPORTS_DIR,
    f"enterprise_ai_governance_{timestamp}.csv"
)


governance_fields = [
    "name",
    "department",
    "tool",
    "days_since_activity",
    "licence_cost_eur",
    "input_tokens",
    "output_tokens",
    "cached_tokens",
    "uncached_tokens",
    "total_tokens",
    "request_count",
    "user_token_limit",
    "usage_percentage",
    "usage_status",
    "estimated_spend_eur",
    "licence_review",
    "potential_savings_eur",
    "anomaly"
]


with open(
    governance_filename,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=governance_fields
    )

    writer.writeheader()

    for user in users:

        writer.writerow(
            {
                field: user[field]
                for field in governance_fields
            }
        )


# ============================================================
# 17. EXPORT DEPARTMENT FORECAST
# ============================================================

forecast_filename = os.path.join(
    REPORTS_DIR,
    "department_forecast.csv"
)


forecast_fields = [
    "department",
    "users",
    "tokens_used",
    "token_limit",
    "current_usage_percentage",
    "forecast_tokens",
    "forecast_usage_percentage",
    "warning_threshold_percent",
    "critical_threshold_percent",
    "requests",
    "current_spend_eur",
    "forecast_spend_eur",
    "monthly_budget_eur",
    "forecast_budget_percentage",
    "licence_cost_eur",
    "potential_savings_eur",
    "forecast_status",
    "management_implication"
]


with open(
    forecast_filename,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=forecast_fields
    )

    writer.writeheader()

    for department, values in department_data.items():

        row = {
            "department": department
        }

        for field in forecast_fields:

            if field != "department":

                row[field] = values.get(
                    field,
                    ""
                )

        writer.writerow(row)


# ============================================================
# 18. EXPORT LATEST AI RECOMMENDATION
# ============================================================

recommendation_filename = os.path.join(
    REPORTS_DIR,
    "latest_ai_governance_recommendation.txt"
)


with open(
    recommendation_filename,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "ENTERPRISE AI USAGE, LICENCE & COST GOVERNANCE\n"
    )

    file.write(
        "Synthetic Demonstration Dataset\n"
    )

    file.write(
        "=" * 55
    )

    file.write("\n\n")

    file.write(ai_recommendation)


# ============================================================
# 19. FINAL OUTPUT
# ============================================================

print()
print("REPORTS CREATED")
print("=" * 55)

print(
    governance_filename
)

print(
    forecast_filename
)

print(
    recommendation_filename
)