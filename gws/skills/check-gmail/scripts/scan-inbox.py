#!/usr/bin/env python3
"""
Gmail inbox scanner — single Python pipeline.

Avoids shell iteration bugs (lesson 4), metadata format limitations (lesson 2),
and tail-stripping breakage (lesson 3). Uses gws-claude.sh wrapper (lesson 1).

Outputs clean JSON to stdout. Progress to stderr.

Usage: python3 scan-inbox.py [maxResults] [account]

  account: "personal" (default) | "ireland" | "cct"
"""

import json
import os
import subprocess
import sys

ACCOUNT_MAP = {
    "personal": os.path.expanduser("~/.brain/integrations/gws/gws-claude.sh"),
    "ireland": os.path.expanduser("~/.brain/integrations/gws-ireland/gws-claude.sh"),
    "cct": os.path.expanduser("~/.brain/integrations/gws-cct/gws-claude.sh"),
}

# Parse args: scan-inbox.py [maxResults] [account]
MAX_RESULTS = 50
ACCOUNT = "personal"

for arg in sys.argv[1:]:
    if arg.isdigit():
        MAX_RESULTS = int(arg)
    elif arg in ACCOUNT_MAP:
        ACCOUNT = arg

GWS = ACCOUNT_MAP[ACCOUNT]


def gws_call(args, params=None, body=None):
    """Call GWS CLI via wrapper. Returns parsed JSON."""
    cmd = [GWS] + args
    if params:
        cmd += ["--params", json.dumps(params)]
    if body:
        cmd += ["--json", json.dumps(body)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout.strip()

    if not output:
        print(f"Error: empty response from GWS CLI", file=sys.stderr)
        print(f"stderr: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Parse JSON directly — no tail stripping (wrapper outputs clean JSON)
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        # Fallback: skip first line if bare gws added a status line
        lines = output.split("\n", 1)
        if len(lines) > 1:
            try:
                data = json.loads(lines[1])
            except json.JSONDecodeError:
                pass
            else:
                # Check for API error in fallback-parsed JSON
                if "error" in data:
                    err = data["error"]
                    print(f"API error ({err.get('code', '?')}): {err.get('message', 'unknown')}", file=sys.stderr)
                    sys.exit(1)
                return data
        print(f"Error: invalid JSON from GWS CLI", file=sys.stderr)
        print(f"stdout (first 500 chars): {output[:500]}", file=sys.stderr)
        sys.exit(1)

    # Check for API error responses (e.g. network failures, auth errors)
    if "error" in data:
        err = data["error"]
        print(f"API error ({err.get('code', '?')}): {err.get('message', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    return data


def extract_header(headers, name):
    """Extract a specific header value from Gmail headers list."""
    return next((h["value"] for h in headers if h["name"] == name), "?")


def extract_email(from_header):
    """Extract email address from From header ('Name <email>' format)."""
    if "<" in from_header and ">" in from_header:
        return from_header.split("<")[1].split(">")[0].strip().lower()
    return from_header.strip().lower()


# --- Pre-flight auth check ---
print(f"Pre-flight: checking auth ({ACCOUNT})...", file=sys.stderr)
try:
    profile = gws_call(["gmail", "users", "getProfile"], params={"userId": "me"})
    email = profile.get("emailAddress", "unknown")
    print(f"Auth OK: {email}", file=sys.stderr)
except SystemExit:
    print(f"\nAuth failed for account: {ACCOUNT}", file=sys.stderr)
    sys.exit(1)

# --- List inbox messages ---
print(f"Fetching inbox (max {MAX_RESULTS})...", file=sys.stderr)
data = gws_call(
    ["gmail", "users", "messages", "list"],
    params={"userId": "me", "q": "in:inbox", "maxResults": MAX_RESULTS},
)
messages = data.get("messages", [])
print(f"Found {len(messages)} messages", file=sys.stderr)

if not messages:
    print("Inbox is empty!", file=sys.stderr)
    json.dump([], sys.stdout)
    sys.exit(0)

# --- Fetch each message with format: full ---
# Using format: full because format: metadata silently drops metadataHeaders
# when passed via GWS CLI (array params are not forwarded to the API).
results = []
for i, msg in enumerate(messages):
    detail = gws_call(
        ["gmail", "users", "messages", "get"],
        params={"userId": "me", "id": msg["id"], "format": "full"},
    )
    headers = detail.get("payload", {}).get("headers", [])
    from_raw = extract_header(headers, "From")

    results.append({
        "id": msg["id"],
        "from_raw": from_raw,
        "from_email": extract_email(from_raw),
        "subject": extract_header(headers, "Subject"),
        "custom_labels": [l for l in detail.get("labelIds", []) if l.startswith("Label_")],
        "all_labels": detail.get("labelIds", []),
    })

    if (i + 1) % 10 == 0:
        print(f"  Fetched {i + 1}/{len(messages)}...", file=sys.stderr)

print(f"Scan complete: {len(results)} messages processed", file=sys.stderr)
json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
