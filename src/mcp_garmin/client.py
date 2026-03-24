"""Garmin Connect client using garminconnect library for health & fitness API access."""

import logging
import os
from pathlib import Path
from typing import Any

from garminconnect import Garmin

logger = logging.getLogger(__name__)

DEFAULT_TOKEN_DIR = "~/.garminconnect"


class GarminAPIError(Exception):
    """Base exception for Garmin Connect API errors."""

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(message)
        self.details = details


class GarminAuthenticationError(GarminAPIError):
    """Authentication error."""


class GarminClient:
    """Client for Garmin Connect API using garminconnect library."""

    def __init__(self) -> None:
        """Initialize Garmin Connect client."""
        self._client: Garmin | None = None
        self._token_dir = os.getenv("GARMINTOKENS", DEFAULT_TOKEN_DIR)

    def _get_client(self) -> Garmin:
        """Get or create authenticated Garmin client.

        Returns:
            Authenticated Garmin client

        Raises:
            GarminAuthenticationError: If authentication fails
        """
        if self._client is not None:
            return self._client

        email = os.getenv("GARMIN_EMAIL")
        password = os.getenv("GARMIN_PASSWORD")

        token_dir = str(Path(self._token_dir).expanduser())

        try:
            client = Garmin(email, password)
            try:
                client.login(tokenstore=token_dir)
            except FileNotFoundError:
                # No tokens found — user must run 'mcp-garmin-init' first
                raise GarminAuthenticationError(
                    "No existing tokens found. Run 'mcp-garmin-init' first to authenticate (supports 2FA)."
                )
            self._client = client
            return client
        except GarminAuthenticationError:
            raise
        except Exception as e:
            raise GarminAuthenticationError(f"Failed to authenticate: {e}") from e

    def check_auth(self) -> dict[str, Any]:
        """Check if there's an active authenticated session.

        Returns:
            Dictionary with authentication status and user info
        """
        token_path = Path(self._token_dir).expanduser()
        if not token_path.exists():
            return {
                "authenticated": False,
                "message": "No token directory found. Set GARMIN_EMAIL and GARMIN_PASSWORD env vars.",
            }

        try:
            client = self._get_client()
            return {
                "authenticated": True,
                "message": "Valid Garmin Connect session",
                "user": {
                    "display_name": client.display_name,
                    "full_name": client.full_name,
                },
            }
        except Exception as e:
            logger.error(f"Auth check failed: {e}")

        return {
            "authenticated": False,
            "message": "Invalid or expired session",
        }

    def login(self) -> dict[str, Any]:
        """Authenticate with Garmin Connect.

        Returns:
            Dictionary with authentication status
        """
        try:
            client = self._get_client()
            return {
                "status": "success",
                "message": "Successfully authenticated with Garmin Connect",
                "display_name": client.display_name,
                "full_name": client.full_name,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    # ── Daily Health & Activity ──────────────────────────────

    def get_stats(self, cdate: str) -> dict[str, Any]:
        """Get user daily summary stats.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Daily summary dictionary
        """
        client = self._get_client()
        return client.get_stats(cdate)

    def get_heart_rates(self, cdate: str) -> dict[str, Any]:
        """Get heart rate data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Heart rate data dictionary
        """
        client = self._get_client()
        return client.get_heart_rates(cdate)

    def get_sleep_data(self, cdate: str) -> dict[str, Any]:
        """Get sleep data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Sleep data dictionary
        """
        client = self._get_client()
        return client.get_sleep_data(cdate)

    def get_stress_data(self, cdate: str) -> dict[str, Any]:
        """Get all-day stress data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Stress data dictionary
        """
        client = self._get_client()
        return client.get_all_day_stress(cdate)

    def get_steps_data(self, cdate: str) -> list[dict[str, Any]]:
        """Get steps data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Steps data list
        """
        client = self._get_client()
        return client.get_steps_data(cdate)

    def get_body_battery(self, cdate: str) -> list[dict[str, Any]]:
        """Get body battery data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Body battery data list
        """
        client = self._get_client()
        return client.get_body_battery(cdate)

    def get_respiration_data(self, cdate: str) -> dict[str, Any]:
        """Get respiration data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Respiration data dictionary
        """
        client = self._get_client()
        return client.get_respiration_data(cdate)

    def get_spo2_data(self, cdate: str) -> dict[str, Any]:
        """Get SpO2 data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            SpO2 data dictionary
        """
        client = self._get_client()
        return client.get_spo2_data(cdate)

    def get_hydration_data(self, cdate: str) -> dict[str, Any]:
        """Get hydration data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Hydration data dictionary
        """
        client = self._get_client()
        return client.get_hydration_data(cdate)

    # ── Advanced Health Metrics ──────────────────────────────

    def get_hrv_data(self, cdate: str) -> dict[str, Any] | None:
        """Get Heart Rate Variability data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            HRV data dictionary or None
        """
        client = self._get_client()
        return client.get_hrv_data(cdate)

    def get_training_readiness(self, cdate: str) -> dict[str, Any]:
        """Get training readiness data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Training readiness data
        """
        client = self._get_client()
        return client.get_training_readiness(cdate)

    def get_training_status(self, cdate: str) -> dict[str, Any]:
        """Get training status data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Training status data
        """
        client = self._get_client()
        return client.get_training_status(cdate)

    def get_max_metrics(self, cdate: str) -> dict[str, Any]:
        """Get max metrics (VO2Max) for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Max metrics data
        """
        client = self._get_client()
        return client.get_max_metrics(cdate)

    def get_endurance_score(self, cdate: str) -> dict[str, Any]:
        """Get endurance score for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Endurance score data
        """
        client = self._get_client()
        return client.get_endurance_score(cdate)

    def get_hill_score(self, cdate: str) -> dict[str, Any]:
        """Get hill score for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Hill score data
        """
        client = self._get_client()
        return client.get_hill_score(cdate)

    def get_fitnessage(self, cdate: str) -> dict[str, Any]:
        """Get fitness age data for a date.

        Args:
            cdate: Date in YYYY-MM-DD format

        Returns:
            Fitness age data
        """
        client = self._get_client()
        return client.get_fitnessage_data(cdate)

    # ── Historical Data & Trends ─────────────────────────────

    def get_daily_steps(self, start: str, end: str) -> list[dict[str, Any]]:
        """Get daily steps in a date range.

        Args:
            start: Start date in YYYY-MM-DD format
            end: End date in YYYY-MM-DD format

        Returns:
            List of daily step data
        """
        client = self._get_client()
        return client.get_daily_steps(start, end)

    def get_weekly_steps(self, end: str, weeks: int = 52) -> list[dict[str, Any]]:
        """Get weekly steps aggregates.

        Args:
            end: End date in YYYY-MM-DD format
            weeks: Number of weeks to fetch (default: 52)

        Returns:
            List of weekly step aggregates
        """
        client = self._get_client()
        return client.get_weekly_steps(end, weeks)

    def get_weekly_stress(self, end: str, weeks: int = 52) -> list[dict[str, Any]]:
        """Get weekly stress aggregates.

        Args:
            end: End date in YYYY-MM-DD format
            weeks: Number of weeks to fetch (default: 52)

        Returns:
            List of weekly stress aggregates
        """
        client = self._get_client()
        return client.get_weekly_stress(end, weeks)

    # ── Body Composition & Weight ────────────────────────────

    def get_body_composition(
        self, startdate: str, enddate: str | None = None
    ) -> dict[str, Any]:
        """Get body composition data.

        Args:
            startdate: Start date in YYYY-MM-DD format
            enddate: End date in YYYY-MM-DD format (optional, defaults to startdate)

        Returns:
            Body composition data
        """
        client = self._get_client()
        return client.get_body_composition(startdate, enddate)

    def get_weigh_ins(self, startdate: str, enddate: str) -> dict[str, Any]:
        """Get weigh-ins between dates.

        Args:
            startdate: Start date in YYYY-MM-DD format
            enddate: End date in YYYY-MM-DD format

        Returns:
            Weigh-in data
        """
        client = self._get_client()
        return client.get_weigh_ins(startdate, enddate)

    # ── Activities & Workouts ────────────────────────────────

    def get_activities(
        self, start: int = 0, limit: int = 20, activitytype: str | None = None
    ) -> list[dict[str, Any]]:
        """Get recent activities.

        Args:
            start: Starting offset (0 = most recent)
            limit: Number of activities to return
            activitytype: Optional activity type filter

        Returns:
            List of activities
        """
        client = self._get_client()
        result = client.get_activities(start, limit, activitytype)
        if isinstance(result, list):
            return result
        if isinstance(result, dict) and "activityList" in result:
            return result["activityList"]
        return []

    def get_activities_by_date(
        self,
        startdate: str,
        enddate: str | None = None,
        activitytype: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get activities between specific dates.

        Args:
            startdate: Start date in YYYY-MM-DD format
            enddate: End date in YYYY-MM-DD format (optional)
            activitytype: Optional activity type filter

        Returns:
            List of activities
        """
        client = self._get_client()
        return client.get_activities_by_date(startdate, enddate, activitytype)

    def get_activity(self, activity_id: str) -> dict[str, Any]:
        """Get activity summary by ID.

        Args:
            activity_id: Garmin activity ID

        Returns:
            Activity summary dictionary
        """
        client = self._get_client()
        return client.get_activity(activity_id)

    def get_activity_details(self, activity_id: str) -> dict[str, Any]:
        """Get detailed activity data.

        Args:
            activity_id: Garmin activity ID

        Returns:
            Activity details dictionary
        """
        client = self._get_client()
        return client.get_activity_details(activity_id)

    def get_last_activity(self) -> dict[str, Any] | None:
        """Get the most recent activity.

        Returns:
            Last activity dictionary or None
        """
        client = self._get_client()
        return client.get_last_activity()

    # ── Goals & Achievements ─────────────────────────────────

    def get_personal_record(self) -> dict[str, Any]:
        """Get personal records.

        Returns:
            Personal records data
        """
        client = self._get_client()
        return client.get_personal_record()

    def get_earned_badges(self) -> list[dict[str, Any]]:
        """Get earned badges.

        Returns:
            List of earned badges
        """
        client = self._get_client()
        return client.get_earned_badges()

    def get_goals(self, status: str = "active") -> list[dict[str, Any]]:
        """Get user goals.

        Args:
            status: Goal status filter (active, future, past)

        Returns:
            List of goals
        """
        client = self._get_client()
        return client.get_goals(status)

    # ── Devices & Technical ──────────────────────────────────

    def get_devices(self) -> list[dict[str, Any]]:
        """Get connected devices.

        Returns:
            List of device dictionaries
        """
        client = self._get_client()
        return client.get_devices()

    def get_device_last_used(self) -> dict[str, Any]:
        """Get last used device.

        Returns:
            Last used device data
        """
        client = self._get_client()
        return client.get_device_last_used()

    # ── User Profile ─────────────────────────────────────────

    def get_user_profile(self) -> dict[str, Any]:
        """Get user profile settings.

        Returns:
            User profile data
        """
        client = self._get_client()
        return client.get_user_profile()

    # ── Formatting helpers ───────────────────────────────────

    def format_activity_summary(self, activity: dict[str, Any]) -> str:
        """Format an activity into a readable summary line."""
        name = activity.get("activityName", "Unnamed")
        atype = activity.get("activityType", {}).get("typeKey", "unknown")
        distance_m = activity.get("distance", 0) or 0
        distance_km = distance_m / 1000
        duration_s = activity.get("duration", 0) or 0
        duration_min = int(duration_s // 60)
        calories = activity.get("calories", 0) or 0
        avg_hr = activity.get("averageHR", "N/A")
        start = activity.get("startTimeLocal", "N/A")
        aid = activity.get("activityId", "N/A")

        return (
            f"🏃 {name} ({atype})\n"
            f"   Date: {start}\n"
            f"   Distance: {distance_km:.2f} km\n"
            f"   Duration: {duration_min} min\n"
            f"   Calories: {calories}\n"
            f"   Avg HR: {avg_hr}\n"
            f"   ID: {aid}"
        )
