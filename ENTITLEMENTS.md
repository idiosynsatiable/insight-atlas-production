# Insight Atlas Entitlements Guide

This document outlines the different subscription plans, their associated entitlements, and where these rules are enforced in the codebase.

## 1. Plan Matrix

The application offers three primary plans:

| Feature / Limit        | Free Plan      | Pro Monthly Plan | Pro Yearly Plan  |
| ---------------------- | -------------- | ---------------- | ---------------- |
| **Price**              | $0             | $19 / month      | $190 / year      |
| **Account Creation**   | ✓              | ✓                | ✓                |
| **Intake Sessions**    | 0 per day      | Unlimited        | Unlimited        |
| **Report Generation**  | ✗              | Unlimited        | Unlimited        |
| **LLM Narrative Polish** | ✗              | ✓                | ✓                |
| **Data Export/Purge**  | ✓              | ✓                | ✓                |
| **Stripe Plan ID**     | `N/A`          | `pro_monthly`    | `pro_yearly`     |

## 2. Enforcement Points

Entitlements are enforced in the backend API to ensure security and consistency.

### Core Entitlement Check

-   **File**: `backend/app/main.py`
-   **Function**: `_require_pro(db: Session, user: User)`

This function is the central gate for all Pro-level features. It is used as a dependency in API endpoints that require a paid subscription.

-   It checks if the user has a subscription record with a `plan` that starts with `"pro"` and a `status` of `"active"`.
-   If `DEMO_MODE` is `true`, this check is bypassed to allow for easy testing.
-   If the user does not meet the criteria, it raises a `402 Payment Required` HTTP exception.

### Feature-Specific Enforcement

| Feature                | API Endpoint(s)                                | Enforcement Mechanism                                     |
| ---------------------- | ---------------------------------------------- | --------------------------------------------------------- |
| **Intake Sessions**    | `POST /intake`                                 | `_require_pro()` dependency.                              |
| **Report Generation**  | `POST /analyze/{session_id}`                   | `_require_pro()` dependency.                              |
| **LLM Narrative Polish** | `polish_narrative()` function in `llm_polisher.py` | The function checks if `settings.OPENAI_POLISH_ENABLED` is `true`. This setting should only be enabled in environments where a Pro plan is expected (i.e., not on a free tier). The UI should also hide the toggle for non-Pro users. |

## 3. Subscription Lifecycle Management

-   **File**: `backend/app/stripe_webhook.py`

Subscription status is managed automatically via Stripe webhooks.

-   `checkout.session.completed`: When a user successfully completes a purchase, this event creates or updates their `Subscription` record, setting their `plan` and `status` to `"active"`.
-   `customer.subscription.updated`: Handles changes like upgrades, downgrades, or cancellations. It updates the `status` in our database to reflect the Stripe subscription status.
-   `customer.subscription.deleted`: When a subscription is canceled and the period ends, this event sets the user's plan back to `"free"` and status to `"canceled"`.

This ensures that a user who cancels their subscription will lose Pro access at the end of their billing period, as their status will no longer be `"active"`.
