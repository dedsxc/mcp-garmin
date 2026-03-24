# MCP Garmin Connect 🏃

Model Context Protocol (MCP) server for Garmin Connect. Enables AI assistants (Claude, etc.) to access Garmin health & fitness data: daily stats, heart rate, sleep, stress, activities, body composition, and more.

> **Note**: Uses [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) which wraps Garmin Connect's internal APIs via [Garth](https://github.com/matin/garth) OAuth.

## Installation

```bash
git clone https://github.com/yourusername/mcp-garmin.git
cd mcp-garmin
pip install -e .
```

## Configuration

### 1. Authentication

Set environment variables:

```bash
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"
```

First-time login generates tokens stored in `~/.garminconnect` (valid for ~1 year).

To use a custom token directory:

```bash
export GARMINTOKENS="/path/to/tokens"
```

### 2. Claude Desktop

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "garmin": {
      "command": "mcp-garmin",
      "env": {
        "GARMIN_EMAIL": "your-email@example.com",
        "GARMIN_PASSWORD": "your-password"
      }
    }
  }
}
```

## Available Tools

**Authentication**
- `garmin_login()` - Authenticate with Garmin Connect
- `check_auth()` - Check authentication status

**Daily Health & Activity**
- `get_daily_stats(cdate)` - Daily summary (steps, calories, distance)
- `get_heart_rates(cdate)` - Heart rate data
- `get_sleep_data(cdate)` - Sleep data
- `get_stress_data(cdate)` - Stress data
- `get_steps_data(cdate)` - Detailed steps data
- `get_body_battery(cdate)` - Body battery data
- `get_respiration_data(cdate)` - Respiration data
- `get_spo2_data(cdate)` - SpO2 (blood oxygen) data
- `get_hydration_data(cdate)` - Hydration data

**Advanced Health Metrics**
- `get_hrv_data(cdate)` - Heart Rate Variability
- `get_training_readiness(cdate)` - Training readiness score
- `get_training_status(cdate)` - Training status
- `get_max_metrics(cdate)` - VO2 Max and max metrics
- `get_endurance_score(cdate)` - Endurance score
- `get_hill_score(cdate)` - Hill score
- `get_fitnessage(cdate)` - Fitness age

**Historical Data & Trends**
- `get_daily_steps(start, end)` - Daily steps over range
- `get_weekly_steps(end, weeks)` - Weekly step aggregates
- `get_weekly_stress(end, weeks)` - Weekly stress aggregates

**Activities & Workouts**
- `get_activities(start, limit, activitytype)` - Recent activities
- `get_activities_by_date(startdate, enddate, activitytype)` - Activities by date range
- `get_activity(activity_id)` - Activity summary
- `get_activity_details(activity_id)` - Detailed activity metrics
- `get_last_activity()` - Most recent activity

**Body Composition & Weight**
- `get_body_composition(startdate, enddate)` - Body composition data
- `get_weigh_ins(startdate, enddate)` - Weigh-in records

**Goals & Achievements**
- `get_personal_record()` - Personal records
- `get_earned_badges()` - Earned badges
- `get_goals(status)` - User goals

**Devices**
- `get_devices()` - Connected devices
- `get_device_last_used()` - Last used device

**User Profile**
- `get_user_profile()` - Profile and settings

## Transport Modes

### stdio (default - for Claude Desktop)
```bash
mcp-garmin
```

### SSE (Server-Sent Events)
```bash
mcp-garmin-sse  # Runs on http://0.0.0.0:8000/sse
```

### HTTP Streamable
```bash
mcp-garmin-http  # Runs on http://127.0.0.1:8000/mcp
```

## Pre-commit

Pre-requisite
```bash
python3 -m pip install pre-commit
# Detect-secrets
python3 -m pip install detect-secrets
secrets-secrets scan > .secrets.baseline
```

```bash
pre-commit install
```

## Enforcing conventional commit

This repo follows the angular [conventional commits](https://conventionalcommits.org/).
