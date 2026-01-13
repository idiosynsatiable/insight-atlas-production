#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, sys
import urllib.request

def req(method: str, url: str, token: str | None = None, body: dict | None = None):
    data = None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="ignore")
        raise SystemExit(f"HTTP {e.code}: {msg}")

def main():
    ap = argparse.ArgumentParser(prog="atlasctl", description="Insight Atlas CLI")
    ap.add_argument("--api", default=os.getenv("ATLAS_API", "http://localhost:8000"), help="API base URL")
    ap.add_argument("--token", default=os.getenv("ATLAS_TOKEN"), help="JWT token")

    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("register")
    r.add_argument("email")
    r.add_argument("password")

    l = sub.add_parser("login")
    l.add_argument("email")
    l.add_argument("password")

    m = sub.add_parser("me")

    i = sub.add_parser("intake")
    i.add_argument("--consent", action="store_true", required=True)
    i.add_argument("--survey", default="{}", help="JSON string or @path.json")
    i.add_argument("--text", default="", help="Free text")

    a = sub.add_parser("analyze")
    a.add_argument("session_id", type=int)

    lr = sub.add_parser("reports")

    b = sub.add_parser("billing")
    b.add_argument("plan", choices=["monthly","yearly"])

    args = ap.parse_args()
    api = args.api.rstrip("/")

    if args.cmd == "register":
        out = req("POST", f"{api}/auth/register", body={"email": args.email, "password": args.password})
        print(json.dumps(out, indent=2))
        return
    if args.cmd == "login":
        out = req("POST", f"{api}/auth/login", body={"email": args.email, "password": args.password})
        print(json.dumps(out, indent=2))
        return

    if not args.token:
        raise SystemExit("Missing --token or ATLAS_TOKEN")

    if args.cmd == "me":
        out = req("GET", f"{api}/me", token=args.token)
        print(json.dumps(out, indent=2))
        return

    if args.cmd == "intake":
        survey_raw = args.survey
        if survey_raw.startswith("@"):
            with open(survey_raw[1:], "r", encoding="utf-8") as f:
                survey = json.load(f)
        else:
            survey = json.loads(survey_raw)
        out = req("POST", f"{api}/intake", token=args.token, body={"consent": True, "survey": survey, "free_text": args.text})
        print(json.dumps(out, indent=2))
        return

    if args.cmd == "analyze":
        out = req("POST", f"{api}/analyze/{args.session_id}", token=args.token)
        print(json.dumps(out, indent=2))
        return

    if args.cmd == "reports":
        out = req("GET", f"{api}/reports", token=args.token)
        print(json.dumps(out, indent=2))
        return

    if args.cmd == "billing":
        out = req("POST", f"{api}/billing/checkout?plan={args.plan}", token=args.token)
        print(json.dumps(out, indent=2))
        return

if __name__ == "__main__":
    main()
