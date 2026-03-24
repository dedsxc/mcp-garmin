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
def get_workouts(start: int = 0, limit: int = 100) -> str:
    """Get saved workouts from Garmin Connect.

    Args:
        start: Starting offset (default: 0)
        limit: Maximum results (default: 100)

    Returns:
        List of workouts as JSON
    """
    try:
        client = get_client()
        data = client.get_workouts(start, limit)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting workouts")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_workout_by_id(workout_id: str) -> str:
    """Get a specific workout by ID.

    Args:
        workout_id: Garmin workout ID

    Returns:
        Workout data as JSON
    """
    try:
        client = get_client()
        data = client.get_workout_by_id(workout_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def upload_workout(workout_json: str) -> str:
    """Create a workout on Garmin Connect from a JSON definition.

    The JSON must follow the Garmin workout format. Example for a running workout:
    {
        "workoutName": "Easy Run",
        "sportType": {"sportTypeId": 1, "sportTypeKey": "running"},
        "workoutSegments": [{
            "segmentOrder": 1,
            "sportType": {"sportTypeId": 1, "sportTypeKey": "running"},
            "workoutSteps": [{
                "type": "ExecutableStepDTO",
                "stepOrder": 1,
                "stepType": {"stepTypeId": 3, "stepTypeKey": "interval"},
                "endCondition": {"conditionTypeId": 2, "conditionTypeKey": "time"},
                "endConditionValue": 1800.0
            }]
        }]
    }

    Args:
        workout_json: Workout definition as JSON string

    Returns:
        Created workout data as JSON
    """
    try:
        import json as _json
        payload = _json.loads(workout_json)
        client = get_client()
        data = client.upload_workout(payload)
        return f"✅ Workout created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def schedule_workout(workout_id: str, date_str: str) -> str:
    """Schedule a workout on a specific date in the Garmin calendar.

    Args:
        workout_id: Workout ID (from upload_workout or get_workouts)
        date_str: Target date in YYYY-MM-DD format

    Returns:
        Scheduled workout data as JSON
    """
    try:
        client = get_client()
        data = client.schedule_workout(workout_id, date_str)
        return f"✅ Workout {workout_id} scheduled for {date_str}\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error scheduling workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def create_manual_activity(
    activity_name: str,
    type_key: str,
    start_datetime: str,
    time_zone: str,
    distance_km: float,
    duration_min: int,
) -> str:
    """Create a manual activity on Garmin Connect.

    Args:
        activity_name: Name of the activity
        type_key: Activity type key (running, cycling, swimming, hiking, walking, resort_skiing, etc.)
        start_datetime: Start timestamp (format: 2026-03-24T10:00:00.000)
        time_zone: Timezone (e.g. Europe/Paris, America/New_York)
        distance_km: Distance in kilometers
        duration_min: Duration in minutes

    Returns:
        Created activity data as JSON
    """
    try:
        client = get_client()
        data = client.create_manual_activity(
            activity_name=activity_name,
            type_key=type_key,
            start_datetime=start_datetime,
            time_zone=time_zone,
            distance_km=distance_km,
            duration_min=duration_min,
        )
        return f"✅ Activity '{activity_name}' created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating manual activity")
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


@mcp.tool()
def get_userprofile_settings() -> str:
    """Get detailed user profile settings.

    Returns:
        User profile settings as JSON
    """
    try:
        client = get_client()
        data = client.get_userprofile_settings()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting userprofile settings")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_unit_system() -> str:
    """Get user unit system settings (metric/imperial).

    Returns:
        Unit system data as JSON
    """
    try:
        client = get_client()
        data = client.get_unit_system()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting unit system")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_user_summary(cdate: str) -> str:
    """Get user summary for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        User summary as JSON
    """
    try:
        client = get_client()
        data = client.get_user_summary(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting user summary")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_stats_and_body(cdate: str) -> str:
    """Get combined daily stats and body data for a date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Stats and body data as JSON
    """
    try:
        client = get_client()
        data = client.get_stats_and_body(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting stats and body")
        return f"❌ Error: {str(e)}"


# ── Additional Daily Health ──────────────────────────────────


@mcp.tool()
def get_floors(cdate: str) -> str:
    """Get floors climbed data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Floors data as JSON
    """
    try:
        client = get_client()
        data = client.get_floors(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting floors")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_rhr_day(cdate: str) -> str:
    """Get resting heart rate for a specific day.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Resting heart rate data as JSON
    """
    try:
        client = get_client()
        data = client.get_rhr_day(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting resting heart rate")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_intensity_minutes_data(cdate: str) -> str:
    """Get intensity minutes data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Intensity minutes data as JSON
    """
    try:
        client = get_client()
        data = client.get_intensity_minutes_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting intensity minutes")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_weekly_intensity_minutes(start: str, end: str) -> str:
    """Get weekly intensity minutes between dates.

    Args:
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format

    Returns:
        Weekly intensity minutes data as JSON
    """
    try:
        client = get_client()
        data = client.get_weekly_intensity_minutes(start, end)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting weekly intensity minutes")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_body_battery_events(cdate: str) -> str:
    """Get body battery events for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Body battery events as JSON
    """
    try:
        client = get_client()
        data = client.get_body_battery_events(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting body battery events")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_all_day_events(cdate: str) -> str:
    """Get all-day events for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        All-day events as JSON
    """
    try:
        client = get_client()
        data = client.get_all_day_events(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting all-day events")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_lifestyle_logging_data(cdate: str) -> str:
    """Get lifestyle logging data for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Lifestyle logging data as JSON
    """
    try:
        client = get_client()
        data = client.get_lifestyle_logging_data(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting lifestyle logging data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_morning_training_readiness(cdate: str) -> str:
    """Get morning training readiness for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Morning training readiness data as JSON
    """
    try:
        client = get_client()
        data = client.get_morning_training_readiness(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting morning training readiness")
        return f"❌ Error: {str(e)}"


# ── Progress & Predictions ───────────────────────────────────


@mcp.tool()
def get_progress_summary_between_dates(
    startdate: str,
    enddate: str,
    metric: str = "distance",
    groupbyactivities: bool = True,
) -> str:
    """Get progress summary between dates.

    Args:
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format
        metric: Metric to track - distance, duration, elevationGain, calories (default: distance)
        groupbyactivities: Group by activity types (default: True)

    Returns:
        Progress summary as JSON
    """
    try:
        client = get_client()
        data = client.get_progress_summary_between_dates(startdate, enddate, metric, groupbyactivities)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting progress summary")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_race_predictions(
    startdate: str | None = None,
    enddate: str | None = None,
    prediction_type: str | None = None,
) -> str:
    """Get race predictions (5K, 10K, half-marathon, marathon).

    Args:
        startdate: Start date in YYYY-MM-DD format (optional)
        enddate: End date in YYYY-MM-DD format (optional)
        prediction_type: Race type filter (optional)

    Returns:
        Race predictions as JSON
    """
    try:
        client = get_client()
        data = client.get_race_predictions(startdate, enddate, prediction_type)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting race predictions")
        return f"❌ Error: {str(e)}"


# ── Training Plans ───────────────────────────────────────────


@mcp.tool()
def get_training_plans() -> str:
    """Get all training plans (Garmin Coach, etc.).

    Returns:
        Training plans as JSON
    """
    try:
        client = get_client()
        data = client.get_training_plans()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting training plans")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_training_plan_by_id(plan_id: str) -> str:
    """Get a specific training plan by ID.

    Args:
        plan_id: Training plan ID

    Returns:
        Training plan data as JSON
    """
    try:
        client = get_client()
        data = client.get_training_plan_by_id(plan_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting training plan")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_adaptive_training_plan_by_id(plan_id: str) -> str:
    """Get an adaptive training plan by ID.

    Args:
        plan_id: Adaptive training plan ID

    Returns:
        Adaptive training plan data as JSON
    """
    try:
        client = get_client()
        data = client.get_adaptive_training_plan_by_id(plan_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting adaptive training plan")
        return f"❌ Error: {str(e)}"


# ── Activity Details (extended) ──────────────────────────────


@mcp.tool()
def get_activity_splits(activity_id: str) -> str:
    """Get activity splits (e.g., km splits for running).

    Args:
        activity_id: Garmin activity ID

    Returns:
        Activity splits as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_splits(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity splits")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_split_summaries(activity_id: str) -> str:
    """Get activity split summaries.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Activity split summaries as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_split_summaries(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity split summaries")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_typed_splits(activity_id: str) -> str:
    """Get activity typed splits.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Activity typed splits as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_typed_splits(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity typed splits")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_weather(activity_id: str) -> str:
    """Get weather conditions during an activity.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Weather data as JSON (temperature, humidity, wind, etc.)
    """
    try:
        client = get_client()
        data = client.get_activity_weather(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity weather")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_exercise_sets(activity_id: str) -> str:
    """Get exercise sets for a strength training activity.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Exercise sets data as JSON (reps, weight, etc.)
    """
    try:
        client = get_client()
        data = client.get_activity_exercise_sets(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity exercise sets")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_hr_in_timezones(activity_id: str) -> str:
    """Get heart rate time in zones for an activity.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Heart rate zones data as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_hr_in_timezones(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity HR zones")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_power_in_timezones(activity_id: str) -> str:
    """Get power distribution in zones for an activity (cycling).

    Args:
        activity_id: Garmin activity ID

    Returns:
        Power zones data as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_power_in_timezones(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity power zones")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_gear(activity_id: str) -> str:
    """Get gear used for an activity.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Gear data as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_gear(activity_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity gear")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activity_types() -> str:
    """Get all available activity types on Garmin Connect.

    Returns:
        List of activity types as JSON
    """
    try:
        client = get_client()
        data = client.get_activity_types()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activity types")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_activities_fordate(fordate: str) -> str:
    """Get activities for a specific date.

    Args:
        fordate: Date in YYYY-MM-DD format

    Returns:
        Activities for that date as JSON
    """
    try:
        client = get_client()
        data = client.get_activities_fordate(fordate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting activities for date")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def count_activities() -> str:
    """Get total count of activities.

    Returns:
        Activity count as JSON
    """
    try:
        client = get_client()
        data = client.count_activities()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error counting activities")
        return f"❌ Error: {str(e)}"


# ── Activity Management ──────────────────────────────────────


@mcp.tool()
def delete_activity(activity_id: str) -> str:
    """Delete an activity from Garmin Connect.

    Args:
        activity_id: Garmin activity ID

    Returns:
        Deletion status
    """
    try:
        client = get_client()
        data = client.delete_activity(activity_id)
        return f"✅ Activity {activity_id} deleted.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error deleting activity")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def set_activity_name(activity_id: str, title: str) -> str:
    """Rename an activity.

    Args:
        activity_id: Garmin activity ID
        title: New activity name

    Returns:
        Update status
    """
    try:
        client = get_client()
        data = client.set_activity_name(activity_id, title)
        return f"✅ Activity {activity_id} renamed to '{title}'.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error setting activity name")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def set_activity_type(activity_id: str, type_id: int, type_key: str, parent_type_id: int) -> str:
    """Change the type of an activity.

    Args:
        activity_id: Garmin activity ID
        type_id: Activity type ID (use get_activity_types to find IDs)
        type_key: Activity type key (e.g., running, cycling)
        parent_type_id: Parent type ID

    Returns:
        Update status
    """
    try:
        client = get_client()
        data = client.set_activity_type(activity_id, type_id, type_key, parent_type_id)
        return f"✅ Activity {activity_id} type changed to {type_key}.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error setting activity type")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def download_activity(activity_id: str, dl_fmt: str = "tcx") -> str:
    """Download an activity file in a specific format.

    Args:
        activity_id: Garmin activity ID
        dl_fmt: Download format: tcx, gpx, csv, kml, or fit (default: tcx)

    Returns:
        Base64-encoded file content
    """
    import base64
    try:
        client = get_client()
        data = client.download_activity(activity_id, dl_fmt)
        encoded = base64.b64encode(data).decode("utf-8")
        return f"✅ Activity {activity_id} downloaded as {dl_fmt} ({len(data)} bytes).\nBase64: {encoded[:200]}..."
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error downloading activity")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def create_manual_activity_from_json(payload_json: str) -> str:
    """Create a manual activity from a raw JSON payload.

    Args:
        payload_json: Full activity JSON payload as string

    Returns:
        Created activity data as JSON
    """
    try:
        import json as _json
        payload = _json.loads(payload_json)
        client = get_client()
        data = client.create_manual_activity_from_json(payload)
        return f"✅ Activity created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating manual activity from JSON")
        return f"❌ Error: {str(e)}"


# ── Sport-specific Workout Uploads ───────────────────────────


@mcp.tool()
def upload_running_workout(workout_json: str) -> str:
    """Create a running-specific workout on Garmin Connect.

    Args:
        workout_json: Running workout definition as JSON string

    Returns:
        Created workout data as JSON
    """
    try:
        import json as _json
        payload = _json.loads(workout_json)
        client = get_client()
        data = client.upload_running_workout(payload)
        return f"✅ Running workout created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating running workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def upload_cycling_workout(workout_json: str) -> str:
    """Create a cycling-specific workout on Garmin Connect.

    Args:
        workout_json: Cycling workout definition as JSON string

    Returns:
        Created workout data as JSON
    """
    try:
        import json as _json
        payload = _json.loads(workout_json)
        client = get_client()
        data = client.upload_cycling_workout(payload)
        return f"✅ Cycling workout created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating cycling workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def upload_swimming_workout(workout_json: str) -> str:
    """Create a swimming-specific workout on Garmin Connect.

    Args:
        workout_json: Swimming workout definition as JSON string

    Returns:
        Created workout data as JSON
    """
    try:
        import json as _json
        payload = _json.loads(workout_json)
        client = get_client()
        data = client.upload_swimming_workout(payload)
        return f"✅ Swimming workout created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating swimming workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def upload_hiking_workout(workout_json: str) -> str:
    """Create a hiking-specific workout on Garmin Connect.

    Args:
        workout_json: Hiking workout definition as JSON string

    Returns:
        Created workout data as JSON
    """
    try:
        import json as _json
        payload = _json.loads(workout_json)
        client = get_client()
        data = client.upload_hiking_workout(payload)
        return f"✅ Hiking workout created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating hiking workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def upload_walking_workout(workout_json: str) -> str:
    """Create a walking-specific workout on Garmin Connect.

    Args:
        workout_json: Walking workout definition as JSON string

    Returns:
        Created workout data as JSON
    """
    try:
        import json as _json
        payload = _json.loads(workout_json)
        client = get_client()
        data = client.upload_walking_workout(payload)
        return f"✅ Walking workout created!\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error creating walking workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def download_workout(workout_id: str) -> str:
    """Download a workout by ID.

    Args:
        workout_id: Garmin workout ID

    Returns:
        Workout data as JSON
    """
    try:
        client = get_client()
        data = client.download_workout(workout_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error downloading workout")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_scheduled_workout_by_id(scheduled_workout_id: str) -> str:
    """Get a scheduled workout by its ID.

    Args:
        scheduled_workout_id: Scheduled workout ID

    Returns:
        Scheduled workout data as JSON
    """
    try:
        client = get_client()
        data = client.get_scheduled_workout_by_id(scheduled_workout_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting scheduled workout")
        return f"❌ Error: {str(e)}"


# ── Body Data (write) ────────────────────────────────────────


@mcp.tool()
def add_weigh_in(weight: float, unit_key: str = "kg", timestamp: str = "") -> str:
    """Add a weigh-in record.

    Args:
        weight: Weight value
        unit_key: Unit - kg or lbs (default: kg)
        timestamp: Optional timestamp (ISO format)

    Returns:
        Weigh-in data as JSON
    """
    try:
        client = get_client()
        data = client.add_weigh_in(weight, unit_key, timestamp)
        return f"✅ Weigh-in of {weight} {unit_key} recorded.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error adding weigh-in")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def add_body_composition(
    timestamp: str,
    weight: float,
    percent_fat: float | None = None,
    percent_hydration: float | None = None,
    muscle_mass: float | None = None,
    bone_mass: float | None = None,
    bmi: float | None = None,
    metabolic_age: int | None = None,
) -> str:
    """Add body composition data.

    Args:
        timestamp: Timestamp (ISO format)
        weight: Weight in kg
        percent_fat: Body fat percentage (optional)
        percent_hydration: Hydration percentage (optional)
        muscle_mass: Muscle mass in kg (optional)
        bone_mass: Bone mass in kg (optional)
        bmi: BMI value (optional)
        metabolic_age: Metabolic age (optional)

    Returns:
        Body composition data as JSON
    """
    try:
        client = get_client()
        data = client.add_body_composition(
            timestamp, weight, percent_fat, percent_hydration,
            None, bone_mass, muscle_mass, None, None, None, metabolic_age, None, bmi,
        )
        return f"✅ Body composition recorded.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error adding body composition")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def add_hydration_data(value_in_ml: float, cdate: str | None = None) -> str:
    """Add hydration data.

    Args:
        value_in_ml: Amount of water in milliliters
        cdate: Date in YYYY-MM-DD format (optional, defaults to today)

    Returns:
        Hydration data as JSON
    """
    try:
        client = get_client()
        data = client.add_hydration_data(value_in_ml, cdate=cdate)
        return f"✅ {value_in_ml}ml of hydration recorded.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error adding hydration data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_daily_weigh_ins(cdate: str) -> str:
    """Get daily weigh-ins for a specific date.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Daily weigh-ins as JSON
    """
    try:
        client = get_client()
        data = client.get_daily_weigh_ins(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting daily weigh-ins")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def delete_weigh_in(weight_pk: str, cdate: str) -> str:
    """Delete a specific weigh-in record.

    Args:
        weight_pk: Weigh-in primary key
        cdate: Date in YYYY-MM-DD format

    Returns:
        Deletion status
    """
    try:
        client = get_client()
        data = client.delete_weigh_in(weight_pk, cdate)
        return f"✅ Weigh-in {weight_pk} deleted.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error deleting weigh-in")
        return f"❌ Error: {str(e)}"


# ── Blood Pressure ───────────────────────────────────────────


@mcp.tool()
def get_blood_pressure(startdate: str, enddate: str | None = None) -> str:
    """Get blood pressure data.

    Args:
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format (optional)

    Returns:
        Blood pressure data as JSON
    """
    try:
        client = get_client()
        data = client.get_blood_pressure(startdate, enddate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting blood pressure")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def set_blood_pressure(
    systolic: int, diastolic: int, pulse: int, timestamp: str = "", notes: str = ""
) -> str:
    """Record a blood pressure measurement.

    Args:
        systolic: Systolic value (mmHg)
        diastolic: Diastolic value (mmHg)
        pulse: Pulse rate (bpm)
        timestamp: Timestamp (ISO format, optional)
        notes: Notes (optional)

    Returns:
        Blood pressure data as JSON
    """
    try:
        client = get_client()
        data = client.set_blood_pressure(systolic, diastolic, pulse, timestamp, notes)
        return f"✅ Blood pressure {systolic}/{diastolic} recorded.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error setting blood pressure")
        return f"❌ Error: {str(e)}"


# ── Nutrition ────────────────────────────────────────────────


@mcp.tool()
def get_nutrition_daily_food_log(cdate: str) -> str:
    """Get daily food log.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Food log as JSON
    """
    try:
        client = get_client()
        data = client.get_nutrition_daily_food_log(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting food log")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_nutrition_daily_meals(cdate: str) -> str:
    """Get daily meals.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Meals data as JSON
    """
    try:
        client = get_client()
        data = client.get_nutrition_daily_meals(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting daily meals")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_nutrition_daily_settings(cdate: str) -> str:
    """Get nutrition daily settings.

    Args:
        cdate: Date in YYYY-MM-DD format

    Returns:
        Nutrition settings as JSON
    """
    try:
        client = get_client()
        data = client.get_nutrition_daily_settings(cdate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting nutrition settings")
        return f"❌ Error: {str(e)}"


# ── Gear Tracking ────────────────────────────────────────────


@mcp.tool()
def get_gear(user_profile_number: str) -> str:
    """Get user gear (shoes, bikes, equipment).

    Args:
        user_profile_number: User profile number (from get_user_profile)

    Returns:
        Gear list as JSON
    """
    try:
        client = get_client()
        data = client.get_gear(user_profile_number)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting gear")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_gear_stats(gear_uuid: str) -> str:
    """Get statistics for a specific gear item.

    Args:
        gear_uuid: Gear UUID

    Returns:
        Gear stats as JSON (total distance, activities, etc.)
    """
    try:
        client = get_client()
        data = client.get_gear_stats(gear_uuid)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting gear stats")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_gear_activities(gear_uuid: str, limit: int = 1000) -> str:
    """Get activities associated with a gear item.

    Args:
        gear_uuid: Gear UUID
        limit: Maximum results (default: 1000)

    Returns:
        Gear activities as JSON
    """
    try:
        client = get_client()
        data = client.get_gear_activities(gear_uuid, limit)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting gear activities")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_gear_defaults(user_profile_number: str) -> str:
    """Get default gear settings.

    Args:
        user_profile_number: User profile number

    Returns:
        Gear defaults as JSON
    """
    try:
        client = get_client()
        data = client.get_gear_defaults(user_profile_number)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting gear defaults")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def add_gear_to_activity(gear_uuid: str, activity_id: str) -> str:
    """Add gear to an activity.

    Args:
        gear_uuid: Gear UUID
        activity_id: Garmin activity ID

    Returns:
        Update status
    """
    try:
        client = get_client()
        data = client.add_gear_to_activity(gear_uuid, activity_id)
        return f"✅ Gear added to activity {activity_id}.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error adding gear to activity")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def remove_gear_from_activity(gear_uuid: str, activity_id: str) -> str:
    """Remove gear from an activity.

    Args:
        gear_uuid: Gear UUID
        activity_id: Garmin activity ID

    Returns:
        Update status
    """
    try:
        client = get_client()
        data = client.remove_gear_from_activity(gear_uuid, activity_id)
        return f"✅ Gear removed from activity {activity_id}.\n{_fmt_json(data)}"
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error removing gear from activity")
        return f"❌ Error: {str(e)}"


# ── Badges & Challenges ──────────────────────────────────────


@mcp.tool()
def get_available_badges() -> str:
    """Get all available badges.

    Returns:
        Available badges as JSON
    """
    try:
        client = get_client()
        data = client.get_available_badges()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting available badges")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_in_progress_badges() -> str:
    """Get in-progress badges.

    Returns:
        In-progress badges as JSON
    """
    try:
        client = get_client()
        data = client.get_in_progress_badges()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting in-progress badges")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_badge_challenges(start: int = 0, limit: int = 100) -> str:
    """Get badge challenges.

    Args:
        start: Starting offset (default: 0)
        limit: Maximum results (default: 100)

    Returns:
        Badge challenges as JSON
    """
    try:
        client = get_client()
        data = client.get_badge_challenges(start, limit)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting badge challenges")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_adhoc_challenges(start: int = 0, limit: int = 100) -> str:
    """Get ad-hoc challenges.

    Args:
        start: Starting offset (default: 0)
        limit: Maximum results (default: 100)

    Returns:
        Ad-hoc challenges as JSON
    """
    try:
        client = get_client()
        data = client.get_adhoc_challenges(start, limit)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting ad-hoc challenges")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_inprogress_virtual_challenges(start: int = 0, limit: int = 100) -> str:
    """Get in-progress virtual challenges.

    Args:
        start: Starting offset (default: 0)
        limit: Maximum results (default: 100)

    Returns:
        Virtual challenges as JSON
    """
    try:
        client = get_client()
        data = client.get_inprogress_virtual_challenges(start, limit)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting virtual challenges")
        return f"❌ Error: {str(e)}"


# ── Device (extended) ────────────────────────────────────────


@mcp.tool()
def get_device_settings(device_id: str) -> str:
    """Get settings for a specific device.

    Args:
        device_id: Device ID (from get_devices)

    Returns:
        Device settings as JSON
    """
    try:
        client = get_client()
        data = client.get_device_settings(device_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting device settings")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_device_alarms() -> str:
    """Get device alarms.

    Returns:
        Device alarms as JSON
    """
    try:
        client = get_client()
        data = client.get_device_alarms()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting device alarms")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_device_solar_data(device_id: str, startdate: str, enddate: str | None = None) -> str:
    """Get solar data for a device (solar-capable devices only).

    Args:
        device_id: Device ID
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format (optional)

    Returns:
        Solar data as JSON
    """
    try:
        client = get_client()
        data = client.get_device_solar_data(device_id, startdate, enddate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting device solar data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_primary_training_device() -> str:
    """Get the primary training device.

    Returns:
        Primary training device data as JSON
    """
    try:
        client = get_client()
        data = client.get_primary_training_device()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting primary training device")
        return f"❌ Error: {str(e)}"


# ── Running & Cycling Metrics ────────────────────────────────


@mcp.tool()
def get_cycling_ftp() -> str:
    """Get cycling FTP (Functional Threshold Power).

    Returns:
        FTP data as JSON
    """
    try:
        client = get_client()
        data = client.get_cycling_ftp()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting cycling FTP")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_lactate_threshold(
    latest: bool = True,
    start_date: str | None = None,
    end_date: str | None = None,
    aggregation: str = "daily",
) -> str:
    """Get lactate threshold data.

    Args:
        latest: Get only the latest value (default: True)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        aggregation: Aggregation period - daily or weekly (default: daily)

    Returns:
        Lactate threshold data as JSON
    """
    try:
        client = get_client()
        data = client.get_lactate_threshold(latest, start_date, end_date, aggregation)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting lactate threshold")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_running_tolerance(startdate: str, enddate: str, aggregation: str = "weekly") -> str:
    """Get running tolerance data.

    Args:
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format
        aggregation: Aggregation period - daily or weekly (default: weekly)

    Returns:
        Running tolerance data as JSON
    """
    try:
        client = get_client()
        data = client.get_running_tolerance(startdate, enddate, aggregation)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting running tolerance")
        return f"❌ Error: {str(e)}"


# ── Golf ─────────────────────────────────────────────────────


@mcp.tool()
def get_golf_summary(start: int = 0, limit: int = 100) -> str:
    """Get golf summary.

    Args:
        start: Starting offset (default: 0)
        limit: Maximum results (default: 100)

    Returns:
        Golf summary as JSON
    """
    try:
        client = get_client()
        data = client.get_golf_summary(start, limit)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting golf summary")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_golf_scorecard(scorecard_id: str) -> str:
    """Get a golf scorecard.

    Args:
        scorecard_id: Scorecard ID

    Returns:
        Golf scorecard as JSON
    """
    try:
        client = get_client()
        data = client.get_golf_scorecard(scorecard_id)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting golf scorecard")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_golf_shot_data(scorecard_id: str, hole_numbers: str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18") -> str:
    """Get golf shot data for specific holes.

    Args:
        scorecard_id: Scorecard ID
        hole_numbers: Comma-separated hole numbers (default: all 18)

    Returns:
        Golf shot data as JSON
    """
    try:
        client = get_client()
        data = client.get_golf_shot_data(scorecard_id, hole_numbers)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting golf shot data")
        return f"❌ Error: {str(e)}"


# ── Menstrual & Pregnancy ────────────────────────────────────


@mcp.tool()
def get_menstrual_calendar_data(startdate: str, enddate: str) -> str:
    """Get menstrual calendar data.

    Args:
        startdate: Start date in YYYY-MM-DD format
        enddate: End date in YYYY-MM-DD format

    Returns:
        Menstrual calendar data as JSON
    """
    try:
        client = get_client()
        data = client.get_menstrual_calendar_data(startdate, enddate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting menstrual calendar data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_menstrual_data_for_date(fordate: str) -> str:
    """Get menstrual data for a specific date.

    Args:
        fordate: Date in YYYY-MM-DD format

    Returns:
        Menstrual data as JSON
    """
    try:
        client = get_client()
        data = client.get_menstrual_data_for_date(fordate)
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting menstrual data")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def get_pregnancy_summary() -> str:
    """Get pregnancy summary.

    Returns:
        Pregnancy summary as JSON
    """
    try:
        client = get_client()
        data = client.get_pregnancy_summary()
        return _fmt_json(data)
    except GarminAuthenticationError:
        return "❌ Not authenticated. Please use garmin_login() first."
    except Exception as e:
        logger.exception("Error getting pregnancy summary")
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
