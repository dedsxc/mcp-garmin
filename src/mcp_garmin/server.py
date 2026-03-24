"""MCP server implementation for Garmin Connect API using FastMCP."""

import json
import logging
import os

from fastmcp import FastMCP

from .client import GarminAPIError, GarminAuthenticationError, GarminClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-garmin")

# Initialize FastMCP server
mcp = FastMCP("Garmin Connect")

# Global client instance
_client: GarminClient | None = None


def get_client() -> GarminClient:
    """Get or create Garmin client instance."""
    global _client
    if _client is None:
        _client = GarminClient()
    return _client


def _fmt_json(data: object) -> str:
    """Format data as indented JSON string."""
    return json.dumps(data, indent=2, default=str, ensure_ascii=False)


# ── Authentication ───────────────────────────────────────────


@mcp.tool()
def garmin_login() -> str:
    """Authenticate with Garmin Connect.

    Requires GARMIN_EMAIL and GARMIN_PASSWORD environment variables.
    Tokens are stored in ~/.garminconnect (or GARMINTOKENS env var).

    Returns:
        Authentication status message
    """
    try:
        client = get_client()
        result = client.login()

        if result.get("status") == "success":
            return (
                f"✅ {result['message']}\n"
                f"Display Name: {result.get('display_name')}\n"
                f"Full Name: {result.get('full_name')}"
            )
        else:
            return f"❌ {result['message']}"
    except Exception as e:
        logger.exception("Error during login")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def check_auth() -> str:
    """Check current Garmin Connect authentication status.

    Returns:
        Authentication status and user information
    """
    try:
        client = get_client()
        result = client.check_auth()

        if result.get("authenticated"):
            user = result.get("user", {})
            return (
                f"✅ Authenticated with Garmin Connect\n"
                f"Display Name: {user.get('display_name')}\n"
                f"Full Name: {user.get('full_name')}"
            )
        else:
            return f"❌ Not authenticated: {result.get('message')}"
    except Exception as e:
        logger.exception("Error checking auth")
        return f"❌ Error: {str(e)}"


# ── Daily Health & Activity ──────────────────────────────────


@mcp.tool()
def get_daily_stats(cdate: str) -> str:
    """Get daily activity summary (steps, calories, distance, etc).

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Daily summary data as JSON
    """
    try:
        client = get_client()
        data = client.get_stats(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting daily stats")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_heart_rates(cdate: str) -> str:
    """Get heart rate data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Heart rate data as JSON (resting HR, min, max, time in zones)
    """
    try:
        client = get_client()
        data = client.get_heart_rates(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting heart rates")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_sleep_data(cdate: str) -> str:
    """Get sleep data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Sleep data as JSON (duration, phases, score)
    """
    try:
        client = get_client()
        data = client.get_sleep_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting sleep data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_stress_data(cdate: str) -> str:
    """Get all-day stress data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Stress data as JSON
    """
    try:
        client = get_client()
        data = client.get_stress_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting stress data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_steps_data(cdate: str) -> str:
    """Get detailed steps data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Steps data as JSON
    """
    try:
        client = get_client()
        data = client.get_steps_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting steps data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_body_battery(cdate: str) -> str:
    """Get body battery data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Body battery data as JSON
    """
    try:
        client = get_client()
        data = client.get_body_battery(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting body battery")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_respiration_data(cdate: str) -> str:
    """Get respiration data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Respiration data as JSON
    """
    try:
        client = get_client()
        data = client.get_respiration_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting respiration data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_spo2_data(cdate: str) -> str:
    """Get SpO2 (blood oxygen) data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        SpO2 data as JSON
    """
    try:
        client = get_client()
        data = client.get_spo2_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting SpO2 data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_hydration_data(cdate: str) -> str:
    """Get hydration data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Hydration data as JSON
    """
    try:
        client = get_client()
        data = client.get_hydration_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting hydration data")
        return f"❌ Error: {str(e)}"


# ── Advanced Health Metrics ──────────────────────────────────


@mcp.tool()
def get_hrv_data(cdate: str) -> str:
    """Get Heart Rate Variability (HRV) data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        HRV data as JSON
    """
    try:
        client = get_client()
        data = client.get_hrv_data(cdate)
        return _fmt_json(data) if data else "No HRV data available for this date."
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting HRV data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_training_readiness(cdate: str) -> str:
    """Get training readiness score for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Training readiness data as JSON
    """
    try:
        client = get_client()
        data = client.get_training_readiness(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting training readiness")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_training_status(cdate: str) -> str:
    """Get training status data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Training status data as JSON
    """
    try:
        client = get_client()
        data = client.get_training_status(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting training status")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_max_metrics(cdate: str) -> str:
    """Get VO2 Max and other max metrics for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Max metrics data as JSON
    """
    try:
        client = get_client()
        data = client.get_max_metrics(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting max metrics")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_endurance_score(cdate: str) -> str:
    """Get endurance score for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Endurance score data as JSON
    """
    try:
        client = get_client()
        data = client.get_endurance_score(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting endurance score")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_hill_score(cdate: str) -> str:
    """Get hill score for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Hill score data as JSON
    """
    try:
        client = get_client()
        data = client.get_hill_score(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting hill score")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_fitnessage(cdate: str) -> str:
    """Get fitness age data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Fitness age data as JSON
    """
    try:
        client = get_client()
        data = client.get_fitnessage(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting fitness age")
        return f"❌ Error: {str(e)}"


# ── Historical Data & Trends ────────────────────────────────


@mcp.tool()
def get_daily_steps(start: str, end: str) -> str:
    """Get daily steps over a date range.

    Args:
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format

    Returns:
        Daily steps data as JSON
    """
    try:
        client = get_client()
        data = client.get_daily_steps(start, end)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting daily steps")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_weekly_steps(end: str, weeks: int = 52) -> str:
    """Get weekly step aggregates.

    Args:
        end: End date in YYYY-MM-DD format
        weeks: Number of weeks to fetch (default: 52)

    Returns:
        Weekly step aggregates as JSON
    """
    try:
        client = get_client()
        data = client.get_weekly_steps(end, weeks)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting weekly steps")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_weekly_stress(end: str, weeks: int = 52) -> str:
    """Get weekly stress aggregates.

    Args:
        end: End date in YYYY-MM-DD format
        weeks: Number of weeks to fetch (default: 52)

    Returns:
        Weekly stress aggregates as JSON
    """
    try:
        client = get_client()
        data = client.get_weekly_stress(end, weeks)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting weekly stress")
        return f"❌ Error: {str(e)}"


# ── Activities & Workouts ────────────────────────────────────


@mcp.tool()
def get_activities(start: int = 0, limit: int = 20, activitytype: str | None = None) -> str:
    """Get recent activities from Garmin Connect.

    Args:
        start: Starting offset, 0 = most recent (default: 0)
        limit: Number of activities to return (default: 20)
        activitytype: Optional filter (running, cycling, swimming, hiking, walking, etc.)

    Returns:
        Formatted list of activities
    """
    try:
        client = get_client()
        activities = client.get_activities(start, limit, activitytype)

        if not activities:
            return "🏃 No activities found."

        output = [f"🏃 Activities ({len(activities)}):\n"]
        for activity in activities:
            output.append(client.format_activity_summary(activity))
            output.append("")

        return "\n".join(output)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activities")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activities_by_date(
    startdate: str,
    enddate: str | None = None,
    activitytype: str | None = None,
) -> str:
    """Get activities between specific dates.

    Args:
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format (optional)
        activitytype: Optional filter (running, cycling, swimming, hiking, walking, etc.)

    Returns:
        Formatted list of activities
    """
    try:
        client = get_client()
        activities = client.get_activities_by_date(startdate, enddate, activitytype)

        if not activities:
            return f"🏃 No activities found between {startdate} and {enddate or 'now'}."

        output = [f"🏃 Activities from {startdate} to {enddate or 'now'} ({len(activities)}):\n"]
        for activity in activities:
            output.append(client.format_activity_summary(activity))
            output.append("")

        return "\n".join(output)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activities by date")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity(activity_id: str) -> str:
    """Get detailed information about a specific activity.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Activity data as JSON
    """
    try:
        client = get_client()
        data = client.get_activity(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_details(activity_id: str) -> str:
    """Get detailed metrics for a specific activity (charts, polylines).

    Args:
        activity_id: Garmin activity ID

    Returns:
        Activity details as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_details(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity details")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_last_activity() -> str:
    """Get the most recent activity.

    Returns:
        Last activity data as JSON
    """
    try:
        client = get_client()
        data = client.get_last_activity()
        if not data:
            return "🏃 No activities found."
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting last activity")
        return f"❌ Error: {str(e)}"


# ── Body Composition & Weight ────────────────────────────────


@mcp.tool()
def get_body_composition(startdate: str, enddate: str | None = None) -> str:
    """Get body composition data (weight, BMI, body fat, muscle mass, etc).

    Args:
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format (optional, defaults to startdate)

    Returns:
        Body composition data as JSON
    """
    try:
        client = get_client()
        data = client.get_body_composition(startdate, enddate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting body composition")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_weigh_ins(startdate: str, enddate: str) -> str:
    """Get weigh-in records between dates.

    Args:
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format

    Returns:
        Weigh-in data as JSON
    """
    try:
        client = get_client()
        data = client.get_weigh_ins(startdate, enddate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting weigh-ins")
        return f"❌ Error: {str(e)}"


# ── Goals & Achievements ────────────────────────────────────


@mcp.tool()
def get_personal_record() -> str:
    """Get personal records (PRs) for the current user.

    Returns:
        Personal records data as JSON
    """
    try:
        client = get_client()
        data = client.get_personal_record()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting personal records")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_earned_badges() -> str:
    """Get badges earned by the current user.

    Returns:
        Earned badges data as JSON
    """
    try:
        client = get_client()
        data = client.get_earned_badges()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting earned badges")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_goals(status: str = "active") -> str:
    """Get user goals.

    Args:
        status: Goal status filter - active, future, or past (default: active)

    Returns:
        Goals data as JSON
    """
    try:
        client = get_client()
        data = client.get_goals(status)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting goals")
        return f"❌ Error: {str(e)}"


# ── Devices & Technical ──────────────────────────────────────


@mcp.tool()
def get_devices() -> str:
    """Get connected Garmin devices.

    Returns:
        List of devices as JSON
    """
    try:
        client = get_client()
        data = client.get_devices()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting devices")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_device_last_used() -> str:
    """Get the last used Garmin device.

    Returns:
        Last used device data as JSON
    """
    try:
        client = get_client()
        data = client.get_device_last_used()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting last used device")
        return f"❌ Error: {str(e)}"


# ── User Profile ─────────────────────────────────────────────


@mcp.tool()
def get_user_profile() -> str:
    """Get user profile and settings.

    Returns:
        User profile data as JSON
    """
    try:
        client = get_client()
        data = client.get_user_profile()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting user profile")
        return f"❌ Error: {str(e)}"


# ── Server entry points ─────────────────────────────────────


def serve(transport: str = "stdio", host: str = "0.0.0.0", port: int = 8000):
    """Serve the MCP server.

    Args:
        transport: "stdio", "sse", or "streamable-http" (default: stdio)
        host: Host to bind (default: 0.0.0.0)
        port: Port to bind (default: 8000)
    """
    if transport in ("sse", "streamable-http"):
        logger.info(f"Starting MCP server in {transport.upper()} mode on {host}:{port}")
        mcp.run(transport=transport, host=host, port=port)
    else:
        logger.info("Starting MCP server in stdio mode")
        mcp.run()


def main():
    """Entry point for mcp-garmin command (stdio mode)."""
    serve(transport="stdio")


def main_sse():
    """Entry point for mcp-garmin-sse command (SSE mode on /sse)."""
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))
    serve(transport="sse", host=host, port=port)


def main_http():
    """Entry point for mcp-garmin-http command (HTTP mode on /mcp)."""
    serve(transport="streamable-http", host="0.0.0.0", port=8000)
