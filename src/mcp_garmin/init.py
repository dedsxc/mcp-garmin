"""Interactive CLI for initial Garmin Connect authentication (supports MFA/2FA)."""

import os
import sys
from pathlib import Path

from garminconnect import Garmin

DEFAULT_TOKEN_DIR = "~/.garminconnect"


def main():
    """Interactive first-time authentication with Garmin Connect.

    Handles MFA/2FA prompts and saves tokens for server use.
    """
    token_dir = os.getenv("GARMINTOKENS", DEFAULT_TOKEN_DIR)
    token_path = Path(token_dir).expanduser()

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email:
        email = input("Garmin email: ")
    if not password:
        import getpass
        password = getpass.getpass("Garmin password: ")

    print(f"\n🔐 Authenticating with Garmin Connect as {email}...")
    print("   (If you have 2FA enabled, you'll be prompted for the code)\n")

    try:
        client = Garmin(
            email,
            password,
            prompt_mfa=lambda: input("Enter MFA/2FA one-time code: "),
        )
        client.login()

        token_path.mkdir(parents=True, exist_ok=True)
        client.garth.dump(str(token_path))

        print(f"\n✅ Authentication successful!")
        print(f"   Display Name: {client.display_name}")
        print(f"   Full Name: {client.full_name}")
        print(f"   Tokens saved to: {token_path}")
        print(f"\n   You can now start the MCP server with: mcp-garmin-http")

    except Exception as e:
        print(f"\n❌ Authentication failed: {e}", file=sys.stderr)
        sys.exit(1)
