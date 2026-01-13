_# Insight Atlas Runbook_

This runbook provides guidance for handling common incidents, debugging issues, and performing operational tasks.

## 1. Incident Response

### High API Error Rate or Unavailability

1.  **Check Fly.io Status**: Go to `https://fly.io/apps/insight-atlas-api` (or the staging app) and review the logs and metrics.
    ```bash
    fly logs -a <app-name>
    ```
2.  **Check Health Endpoint**: Access `https://<api-domain>/healthz`. If it's down, the instance is likely unhealthy.
3.  **Restart the Application**: A restart can often resolve transient issues.
    ```bash
    fly restart -a <app-name>
    ```
4.  **Check Database Connection**: Verify that the database is reachable and not under heavy load. Check your PostgreSQL provider's dashboard.
5.  **Rollback Deployment**: If the issue started after a recent deployment, roll back to the previous stable version.
    ```bash
    fly releases -a <app-name> # List releases
    fly deploy -a <app-name> -v <previous-version-number>
    ```

### Stripe Webhook Failures

1.  **Check Stripe Dashboard**: Go to Developers > Webhooks in your Stripe dashboard. Look for failed deliveries to your endpoint.
2.  **Inspect Error Logs**: The Stripe dashboard will show the HTTP status code and response body from your API. Use this to identify the error.
3.  **Check API Logs**: Use `fly logs` to find the corresponding request ID and trace the error in the backend logs.
4.  **Common Causes**:
    *   **Invalid Signature**: Ensure `STRIPE_WEBHOOK_SECRET` is set correctly.
    *   **Database Error**: The webhook handler might be failing to write to the database. Check DB connectivity and logs.
    *   **Logic Error**: A bug in one of the `handle_*` functions in `stripe_webhook.py`.
5.  **Retry Failed Events**: Once the issue is fixed, you can manually retry failed webhooks from the Stripe dashboard.

## 2. Debugging

### Debugging a User's Subscription Issue

1.  **Get User Information**: Obtain the user's email address.
2.  **Connect to Production/Staging DB**: Use a secure database client to connect to the appropriate PostgreSQL database.
3.  **Inspect User and Subscription Tables**:
    ```sql
    -- Find the user
    SELECT * FROM "user" WHERE email = 'user@example.com';

    -- Check their subscription status
    SELECT * FROM subscription WHERE user_id = <user_id_from_above>;
    ```
4.  **Cross-reference with Stripe**: Use the `stripe_customer_id` or `stripe_subscription_id` from the `subscription` table to find the customer and their subscription in the Stripe dashboard. Compare the plan and status between your database and Stripe.

### Local Debugging with Production-like Environment

Use the `docker-compose.prod.yml` file to run a local stack with PostgreSQL.

1.  **Start the stack**:
    ```bash
    docker compose -f docker-compose.prod.yml up --build
    ```
2.  This provides a more accurate environment for reproducing bugs that might not appear with SQLite.

## 3. Rollback Procedures

### Backend (Fly.io)

Fly.io keeps a history of all deployed releases. Rolling back is a fast and safe operation.

1.  **List releases** to find the version number of the last known good release:
    ```bash
    fly releases -a <app-name>
    ```
2.  **Deploy the previous version**:
    ```bash
    fly deploy -a <app-name> -v <version-number>
    ```

### Frontend (Vercel)

Vercel also makes rollbacks simple.

1.  Go to your project's **Deployments** tab in the Vercel dashboard.
2.  Find the last known good deployment.
3.  Click the overflow menu (...) and select **Redeploy**.
4.  Alternatively, you can revert the commit in your `main` or `develop` branch and push, which will trigger a new deployment with the old code.
