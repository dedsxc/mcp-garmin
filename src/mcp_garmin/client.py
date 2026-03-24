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

    # ── Workouts & Training ───────────────────────────────────

    def get_workouts(self, start: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get user workouts.

        Args:
            start: Starting offset
            limit: Max results

        Returns:
            List of workout dictionaries
        """
        client = self._get_client()
        return client.get_workouts(start, limit)

    def get_workout_by_id(self, workout_id: str) -> dict[str, Any]:
        """Get a specific workout by ID.

        Args:
            workout_id: Garmin workout ID

        Returns:
            Workout dictionary
        """
        client = self._get_client()
        return client.get_workout_by_id(workout_id)

    def upload_workout(self, workout_json: dict[str, Any]) -> dict[str, Any]:
        """Create/upload a workout from JSON definition.

        Args:
            workout_json: Workout definition as JSON dict

        Returns:
            Created workout data
        """
        client = self._get_client()
        return client.upload_workout(workout_json)

    def schedule_workout(self, workout_id: str, date_str: str) -> dict[str, Any]:
        """Schedule a workout on a specific date.

        Args:
            workout_id: Workout ID to schedule
            date_str: Target date in YYYY-MM-DD format

        Returns:
            Scheduled workout data
        """
        client = self._get_client()
        return client.schedule_workout(workout_id, date_str)

    def create_manual_activity(
        self,
        activity_name: str,
        type_key: str,
        start_datetime: str,
        time_zone: str,
        distance_km: float,
        duration_min: int,
    ) -> dict[str, Any]:
        """Create a manual activity.

        Args:
            activity_name: Name of the activity
            type_key: Activity type (running, cycling, swimming, hiking, walking, etc.)
            start_datetime: Start timestamp (format: 2026-03-24T10:00:00.000)
            time_zone: Timezone (e.g. Europe/Paris)
            distance_km: Distance in kilometers
            duration_min: Duration in minutes

        Returns:
            Created activity data
        """
        client = self._get_client()
        return client.create_manual_activity(
            start_datetime=start_datetime,
            time_zone=time_zone,
            type_key=type_key,
            distance_km=distance_km,
            duration_min=duration_min,
            activity_name=activity_name,
        )

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
        """Get user profile settings."""
        client = self._get_client()
        return client.get_user_profile()

    def get_userprofile_settings(self) -> dict[str, Any]:
        """Get user profile settings (detailed)."""
        client = self._get_client()
        return client.get_userprofile_settings()

    def get_full_name(self) -> str:
        """Get user full name."""
        client = self._get_client()
        return client.get_full_name()

    def get_unit_system(self) -> dict[str, Any]:
        """Get unit system settings."""
        client = self._get_client()
        return client.get_unit_system()

    def get_user_summary(self, cdate: str) -> dict[str, Any]:
        """Get user summary for a date."""
        client = self._get_client()
        return client.get_user_summary(cdate)

    def get_stats_and_body(self, cdate: str) -> dict[str, Any]:
        """Get combined stats and body data for a date."""
        client = self._get_client()
        return client.get_stats_and_body(cdate)

    # ── Additional Daily Health ──────────────────────────────

    def get_floors(self, cdate: str) -> dict[str, Any]:
        """Get floors climbed data for a date."""
        client = self._get_client()
        return client.get_floors(cdate)

    def get_rhr_day(self, cdate: str) -> dict[str, Any]:
        """Get resting heart rate for a specific day."""
        client = self._get_client()
        return client.get_rhr_day(cdate)

    def get_intensity_minutes_data(self, cdate: str) -> dict[str, Any]:
        """Get intensity minutes data for a date."""
        client = self._get_client()
        return client.get_intensity_minutes_data(cdate)

    def get_weekly_intensity_minutes(self, start: str, end: str) -> dict[str, Any]:
        """Get weekly intensity minutes between dates."""
        client = self._get_client()
        return client.get_weekly_intensity_minutes(start, end)

    def get_body_battery_events(self, cdate: str) -> dict[str, Any]:
        """Get body battery events for a date."""
        client = self._get_client()
        return client.get_body_battery_events(cdate)

    def get_all_day_events(self, cdate: str) -> dict[str, Any]:
        """Get all-day events for a date."""
        client = self._get_client()
        return client.get_all_day_events(cdate)

    def get_stress_data_raw(self, cdate: str) -> dict[str, Any]:
        """Get raw stress data for a date (from get_stress_data endpoint)."""
        client = self._get_client()
        return client.get_stress_data(cdate)

    def get_lifestyle_logging_data(self, cdate: str) -> dict[str, Any]:
        """Get lifestyle logging data for a date."""
        client = self._get_client()
        return client.get_lifestyle_logging_data(cdate)

    def get_morning_training_readiness(self, cdate: str) -> dict[str, Any]:
        """Get morning training readiness for a date."""
        client = self._get_client()
        return client.get_morning_training_readiness(cdate)

    # ── Progress & Predictions ───────────────────────────────

    def get_progress_summary_between_dates(
        self, startdate: str, enddate: str, metric: str = "distance", groupbyactivities: bool = True
    ) -> dict[str, Any]:
        """Get progress summary between dates."""
        client = self._get_client()
        return client.get_progress_summary_between_dates(startdate, enddate, metric, groupbyactivities)

    def get_race_predictions(
        self, startdate: str | None = None, enddate: str | None = None, _type: str | None = None
    ) -> dict[str, Any]:
        """Get race predictions (5K, 10K, half marathon, marathon)."""
        client = self._get_client()
        return client.get_race_predictions(startdate, enddate, _type)

    # ── Training Plans ───────────────────────────────────────

    def get_training_plans(self) -> list[dict[str, Any]]:
        """Get training plans."""
        client = self._get_client()
        return client.get_training_plans()

    def get_training_plan_by_id(self, plan_id: str) -> dict[str, Any]:
        """Get training plan by ID."""
        client = self._get_client()
        return client.get_training_plan_by_id(plan_id)

    def get_adaptive_training_plan_by_id(self, plan_id: str) -> dict[str, Any]:
        """Get adaptive training plan by ID."""
        client = self._get_client()
        return client.get_adaptive_training_plan_by_id(plan_id)

    # ── Activity Details (extended) ──────────────────────────

    def get_activity_splits(self, activity_id: str) -> dict[str, Any]:
        """Get activity splits (e.g. km splits for running)."""
        client = self._get_client()
        return client.get_activity_splits(activity_id)

    def get_activity_split_summaries(self, activity_id: str) -> dict[str, Any]:
        """Get activity split summaries."""
        client = self._get_client()
        return client.get_activity_split_summaries(activity_id)

    def get_activity_typed_splits(self, activity_id: str) -> dict[str, Any]:
        """Get activity typed splits."""
        client = self._get_client()
        return client.get_activity_typed_splits(activity_id)

    def get_activity_weather(self, activity_id: str) -> dict[str, Any]:
        """Get weather conditions during an activity."""
        client = self._get_client()
        return client.get_activity_weather(activity_id)

    def get_activity_exercise_sets(self, activity_id: str) -> dict[str, Any]:
        """Get exercise sets for an activity (strength training)."""
        client = self._get_client()
        return client.get_activity_exercise_sets(activity_id)

    def get_activity_hr_in_timezones(self, activity_id: str) -> dict[str, Any]:
        """Get heart rate time in zones for an activity."""
        client = self._get_client()
        return client.get_activity_hr_in_timezones(activity_id)

    def get_activity_power_in_timezones(self, activity_id: str) -> dict[str, Any]:
        """Get power distribution in zones for an activity."""
        client = self._get_client()
        return client.get_activity_power_in_timezones(activity_id)

    def get_activity_gear(self, activity_id: str) -> dict[str, Any]:
        """Get gear used for an activity."""
        client = self._get_client()
        return client.get_activity_gear(activity_id)

    def get_activity_types(self) -> list[dict[str, Any]]:
        """Get all available activity types."""
        client = self._get_client()
        return client.get_activity_types()

    def get_activities_fordate(self, fordate: str) -> list[dict[str, Any]]:
        """Get activities for a specific date."""
        client = self._get_client()
        return client.get_activities_fordate(fordate)

    def count_activities(self) -> dict[str, Any]:
        """Get total activity count."""
        client = self._get_client()
        return client.count_activities()

    # ── Activity Management ──────────────────────────────────

    def delete_activity(self, activity_id: str) -> dict[str, Any]:
        """Delete an activity."""
        client = self._get_client()
        return client.delete_activity(activity_id)

    def set_activity_name(self, activity_id: str, title: str) -> dict[str, Any]:
        """Set/rename an activity."""
        client = self._get_client()
        return client.set_activity_name(activity_id, title)

    def set_activity_type(
        self, activity_id: str, type_id: int, type_key: str, parent_type_id: int
    ) -> dict[str, Any]:
        """Set activity type."""
        client = self._get_client()
        return client.set_activity_type(activity_id, type_id, type_key, parent_type_id)

    def download_activity(self, activity_id: str, dl_fmt: str = "tcx") -> bytes:
        """Download an activity file.

        Args:
            activity_id: Activity ID
            dl_fmt: Format - tcx, gpx, csv, kml, or fit

        Returns:
            File content as bytes
        """
        from garminconnect import Garmin as _G
        fmt_map = {
            "tcx": _G.ActivityDownloadFormat.TCX,
            "gpx": _G.ActivityDownloadFormat.GPX,
            "csv": _G.ActivityDownloadFormat.CSV,
            "kml": _G.ActivityDownloadFormat.KML,
            "fit": _G.ActivityDownloadFormat.ORIGINAL,
        }
        fmt = fmt_map.get(dl_fmt.lower(), _G.ActivityDownloadFormat.TCX)
        client = self._get_client()
        return client.download_activity(activity_id, fmt)

    def import_activity(self, activity_path: str) -> dict[str, Any]:
        """Import an activity from a file (FIT, GPX, TCX)."""
        client = self._get_client()
        return client.import_activity(activity_path)

    def upload_activity(self, activity_path: str) -> dict[str, Any]:
        """Upload an activity from a file (FIT, GPX, TCX)."""
        client = self._get_client()
        return client.upload_activity(activity_path)

    def create_manual_activity_from_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a manual activity from a raw JSON payload."""
        client = self._get_client()
        return client.create_manual_activity_from_json(payload)

    # ── Sport-specific Workout Uploads ───────────────────────

    def upload_running_workout(self, workout: dict[str, Any]) -> dict[str, Any]:
        """Upload a running workout."""
        client = self._get_client()
        return client.upload_running_workout(workout)

    def upload_cycling_workout(self, workout: dict[str, Any]) -> dict[str, Any]:
        """Upload a cycling workout."""
        client = self._get_client()
        return client.upload_cycling_workout(workout)

    def upload_swimming_workout(self, workout: dict[str, Any]) -> dict[str, Any]:
        """Upload a swimming workout."""
        client = self._get_client()
        return client.upload_swimming_workout(workout)

    def upload_hiking_workout(self, workout: dict[str, Any]) -> dict[str, Any]:
        """Upload a hiking workout."""
        client = self._get_client()
        return client.upload_hiking_workout(workout)

    def upload_walking_workout(self, workout: dict[str, Any]) -> dict[str, Any]:
        """Upload a walking workout."""
        client = self._get_client()
        return client.upload_walking_workout(workout)

    def download_workout(self, workout_id: str) -> dict[str, Any]:
        """Download a workout by ID."""
        client = self._get_client()
        return client.download_workout(workout_id)

    def get_scheduled_workout_by_id(self, scheduled_workout_id: str) -> dict[str, Any]:
        """Get a scheduled workout by ID."""
        client = self._get_client()
        return client.get_scheduled_workout_by_id(scheduled_workout_id)

    # ── Body Data (write) ────────────────────────────────────

    def add_weigh_in(self, weight: float, unit_key: str = "kg", timestamp: str = "") -> dict[str, Any]:
        """Add a weigh-in."""
        client = self._get_client()
        return client.add_weigh_in(weight, unit_key, timestamp)

    def add_body_composition(
        self, timestamp: str, weight: float,
        percent_fat: float | None = None, percent_hydration: float | None = None,
        visceral_fat_mass: float | None = None, bone_mass: float | None = None,
        muscle_mass: float | None = None, basal_met: float | None = None,
        active_met: float | None = None, physique_rating: float | None = None,
        metabolic_age: int | None = None, visceral_fat_rating: float | None = None,
        bmi: float | None = None,
    ) -> dict[str, Any]:
        """Add body composition data."""
        client = self._get_client()
        return client.add_body_composition(
            timestamp, weight, percent_fat, percent_hydration,
            visceral_fat_mass, bone_mass, muscle_mass, basal_met,
            active_met, physique_rating, metabolic_age, visceral_fat_rating, bmi,
        )

    def add_hydration_data(
        self, value_in_ml: float, timestamp: str | None = None, cdate: str | None = None
    ) -> dict[str, Any]:
        """Add hydration data in milliliters."""
        client = self._get_client()
        return client.add_hydration_data(value_in_ml, timestamp, cdate)

    def get_daily_weigh_ins(self, cdate: str) -> dict[str, Any]:
        """Get daily weigh-ins for a date."""
        client = self._get_client()
        return client.get_daily_weigh_ins(cdate)

    def delete_weigh_in(self, weight_pk: str, cdate: str) -> dict[str, Any]:
        """Delete a weigh-in."""
        client = self._get_client()
        return client.delete_weigh_in(weight_pk, cdate)

    def delete_weigh_ins(self, cdate: str, delete_all: bool = False) -> dict[str, Any]:
        """Delete weigh-ins for a date."""
        client = self._get_client()
        return client.delete_weigh_ins(cdate, delete_all)

    # ── Blood Pressure ───────────────────────────────────────

    def get_blood_pressure(self, startdate: str, enddate: str | None = None) -> dict[str, Any]:
        """Get blood pressure data."""
        client = self._get_client()
        return client.get_blood_pressure(startdate, enddate)

    def set_blood_pressure(
        self, systolic: int, diastolic: int, pulse: int, timestamp: str = "", notes: str = ""
    ) -> dict[str, Any]:
        """Record a blood pressure measurement."""
        client = self._get_client()
        return client.set_blood_pressure(systolic, diastolic, pulse, timestamp, notes)

    def delete_blood_pressure(self, version: str, cdate: str) -> dict[str, Any]:
        """Delete a blood pressure measurement."""
        client = self._get_client()
        return client.delete_blood_pressure(version, cdate)

    # ── Nutrition ────────────────────────────────────────────

    def get_nutrition_daily_food_log(self, cdate: str) -> dict[str, Any]:
        """Get daily food log."""
        client = self._get_client()
        return client.get_nutrition_daily_food_log(cdate)

    def get_nutrition_daily_meals(self, cdate: str) -> dict[str, Any]:
        """Get daily meals."""
        client = self._get_client()
        return client.get_nutrition_daily_meals(cdate)

    def get_nutrition_daily_settings(self, cdate: str) -> dict[str, Any]:
        """Get nutrition daily settings."""
        client = self._get_client()
        return client.get_nutrition_daily_settings(cdate)

    # ── Gear ─────────────────────────────────────────────────

    def get_gear(self, user_profile_number: str) -> list[dict[str, Any]]:
        """Get user gear (shoes, bikes, etc.)."""
        client = self._get_client()
        return client.get_gear(user_profile_number)

    def get_gear_stats(self, gear_uuid: str) -> dict[str, Any]:
        """Get stats for a specific gear item."""
        client = self._get_client()
        return client.get_gear_stats(gear_uuid)

    def get_gear_activities(self, gear_uuid: str, limit: int = 1000) -> list[dict[str, Any]]:
        """Get activities for a specific gear item."""
        client = self._get_client()
        return client.get_gear_activities(gear_uuid, limit)

    def get_gear_defaults(self, user_profile_number: str) -> dict[str, Any]:
        """Get default gear settings."""
        client = self._get_client()
        return client.get_gear_defaults(user_profile_number)

    def add_gear_to_activity(self, gear_uuid: str, activity_id: str) -> dict[str, Any]:
        """Add gear to an activity."""
        client = self._get_client()
        return client.add_gear_to_activity(gear_uuid, activity_id)

    def remove_gear_from_activity(self, gear_uuid: str, activity_id: str) -> dict[str, Any]:
        """Remove gear from an activity."""
        client = self._get_client()
        return client.remove_gear_from_activity(gear_uuid, activity_id)

    def set_gear_default(self, activity_type: str, gear_uuid: str, default_gear: bool = True) -> dict[str, Any]:
        """Set gear as default for an activity type."""
        client = self._get_client()
        return client.set_gear_default(activity_type, gear_uuid, default_gear)

    # ── Badges & Challenges ──────────────────────────────────

    def get_available_badges(self) -> list[dict[str, Any]]:
        """Get available badges."""
        client = self._get_client()
        return client.get_available_badges()

    def get_in_progress_badges(self) -> list[dict[str, Any]]:
        """Get in-progress badges."""
        client = self._get_client()
        return client.get_in_progress_badges()

    def get_badge_challenges(self, start: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get badge challenges."""
        client = self._get_client()
        return client.get_badge_challenges(start, limit)

    def get_available_badge_challenges(self, start: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get available badge challenges."""
        client = self._get_client()
        return client.get_available_badge_challenges(start, limit)

    def get_non_completed_badge_challenges(self, start: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get non-completed badge challenges."""
        client = self._get_client()
        return client.get_non_completed_badge_challenges(start, limit)

    def get_adhoc_challenges(self, start: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get ad-hoc challenges."""
        client = self._get_client()
        return client.get_adhoc_challenges(start, limit)

    def get_inprogress_virtual_challenges(self, start: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get in-progress virtual challenges."""
        client = self._get_client()
        return client.get_inprogress_virtual_challenges(start, limit)

    # ── Device (extended) ────────────────────────────────────

    def get_device_settings(self, device_id: str) -> dict[str, Any]:
        """Get device settings."""
        client = self._get_client()
        return client.get_device_settings(device_id)

    def get_device_alarms(self) -> list[dict[str, Any]]:
        """Get device alarms."""
        client = self._get_client()
        return client.get_device_alarms()

    def get_device_solar_data(self, device_id: str, startdate: str, enddate: str | None = None) -> dict[str, Any]:
        """Get device solar data."""
        client = self._get_client()
        return client.get_device_solar_data(device_id, startdate, enddate)

    def get_primary_training_device(self) -> dict[str, Any]:
        """Get primary training device."""
        client = self._get_client()
        return client.get_primary_training_device()

    # ── Running & Cycling Metrics ────────────────────────────

    def get_cycling_ftp(self) -> dict[str, Any]:
        """Get cycling FTP (Functional Threshold Power)."""
        client = self._get_client()
        return client.get_cycling_ftp()

    def get_lactate_threshold(
        self, latest: bool = True, start_date: str | None = None,
        end_date: str | None = None, aggregation: str = "daily"
    ) -> dict[str, Any]:
        """Get lactate threshold data."""
        client = self._get_client()
        return client.get_lactate_threshold(latest, start_date, end_date, aggregation)

    def get_running_tolerance(self, startdate: str, enddate: str, aggregation: str = "weekly") -> dict[str, Any]:
        """Get running tolerance data."""
        client = self._get_client()
        return client.get_running_tolerance(startdate, enddate, aggregation)

    # ── Golf ─────────────────────────────────────────────────

    def get_golf_summary(self, start: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get golf summary."""
        client = self._get_client()
        return client.get_golf_summary(start, limit)

    def get_golf_scorecard(self, scorecard_id: str) -> dict[str, Any]:
        """Get golf scorecard."""
        client = self._get_client()
        return client.get_golf_scorecard(scorecard_id)

    def get_golf_shot_data(self, scorecard_id: str, hole_numbers: str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18") -> dict[str, Any]:
        """Get golf shot data."""
        client = self._get_client()
        return client.get_golf_shot_data(scorecard_id, hole_numbers)

    # ── Menstrual & Pregnancy ────────────────────────────────

    def get_menstrual_calendar_data(self, startdate: str, enddate: str) -> dict[str, Any]:
        """Get menstrual calendar data."""
        client = self._get_client()
        return client.get_menstrual_calendar_data(startdate, enddate)

    def get_menstrual_data_for_date(self, fordate: str) -> dict[str, Any]:
        """Get menstrual data for a specific date."""
        client = self._get_client()
        return client.get_menstrual_data_for_date(fordate)

    def get_pregnancy_summary(self) -> dict[str, Any]:
        """Get pregnancy summary."""
        client = self._get_client()
        return client.get_pregnancy_summary()

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
