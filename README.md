# MCP Garmin Connect 🏃

Model Context Protocol (MCP) server for Garmin Connect. Enables AI assistants (Claude, etc.) to access and manage Garmin health & fitness data: daily stats, heart rate, sleep, stress, activities, workouts, body composition, and more.

> **Note**: Uses [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) which wraps Garmin Connect's internal APIs via [Garth](https://github.com/matin/garth) OAuth.

## Installation

```bash
git clone https://github.com/yourusername/mcp-garmin.git
cd mcp-garmin
pip install -e .
```

## Authentication

### First-time setup (supports 2FA/MFA)

Run the interactive init command:

```bash
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"

mcp-garmin-init
```

You will be prompted for your MFA/2FA one-time code if enabled on your account. Tokens are saved to `~/.garminconnect` and are valid for approximately 1 year.

> **Tip**: You can also pass credentials interactively — `mcp-garmin-init` will prompt for email/password if the environment variables are not set.

To use a custom token directory:

```bash
export GARMINTOKENS="/path/to/tokens"
```

### Claude Desktop

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

### Authentication

| Tool | Description |
|------|-------------|
| `garmin_login()` | Authenticate with Garmin Connect (loads existing tokens) |
| `check_auth()` | Check authentication status |

### Daily Health & Activity

All date tools accept `cdate` in `YYYY-MM-DD` format.

| Tool | Description |
|------|-------------|
| `get_daily_stats(cdate)` | Daily summary (steps, calories, distance) |
| `get_heart_rates(cdate)` | Heart rate data (resting HR, min, max, zones) |
| `get_sleep_data(cdate)` | Sleep data (duration, phases, score) |
| `get_stress_data(cdate)` | All-day stress data |
| `get_steps_data(cdate)` | Detailed steps data |
| `get_body_battery(cdate)` | Body battery data |
| `get_body_battery_events(cdate)` | Body battery events |
| `get_respiration_data(cdate)` | Respiration data |
| `get_spo2_data(cdate)` | SpO2 (blood oxygen) data |
| `get_hydration_data(cdate)` | Hydration data |
| `get_floors(cdate)` | Floors climbed |
| `get_rhr_day(cdate)` | Resting heart rate |
| `get_intensity_minutes_data(cdate)` | Intensity minutes |
| `get_all_day_events(cdate)` | All-day events |
| `get_lifestyle_logging_data(cdate)` | Lifestyle logging data |

### Advanced Health Metrics

| Tool | Description |
|------|-------------|
| `get_hrv_data(cdate)` | Heart Rate Variability |
| `get_training_readiness(cdate)` | Training readiness score |
| `get_morning_training_readiness(cdate)` | Morning training readiness |
| `get_training_status(cdate)` | Training status |
| `get_max_metrics(cdate)` | VO2 Max and max metrics |
| `get_endurance_score(cdate)` | Endurance score |
| `get_hill_score(cdate)` | Hill score |
| `get_fitnessage(cdate)` | Fitness age |

### Running & Cycling Metrics

| Tool | Description |
|------|-------------|
| `get_race_predictions(startdate, enddate)` | Race predictions (5K, 10K, half, marathon) |
| `get_lactate_threshold(latest, start_date, end_date)` | Lactate threshold |
| `get_running_tolerance(startdate, enddate, aggregation)` | Running tolerance |
| `get_cycling_ftp()` | Cycling FTP (Functional Threshold Power) |

### Historical Data & Trends

| Tool | Description |
|------|-------------|
| `get_daily_steps(start, end)` | Daily steps over a date range |
| `get_weekly_steps(end, weeks)` | Weekly step aggregates |
| `get_weekly_stress(end, weeks)` | Weekly stress aggregates |
| `get_weekly_intensity_minutes(start, end)` | Weekly intensity minutes |
| `get_progress_summary_between_dates(startdate, enddate, metric)` | Progress summary (distance, duration, calories...) |
| `get_user_summary(cdate)` | User summary for a date |
| `get_stats_and_body(cdate)` | Combined stats and body data |

### Activities

| Tool | Description |
|------|-------------|
| `get_activities(start, limit, activitytype)` | Recent activities |
| `get_activities_by_date(startdate, enddate, activitytype)` | Activities by date range |
| `get_activities_fordate(fordate)` | Activities for a specific date |
| `get_activity(activity_id)` | Activity summary |
| `get_activity_details(activity_id)` | Detailed activity metrics (charts, polylines) |
| `get_last_activity()` | Most recent activity |
| `count_activities()` | Total activity count |

### Activity Details (extended)

| Tool | Description |
|------|-------------|
| `get_activity_splits(activity_id)` | Activity splits (km/mile splits) |
| `get_activity_split_summaries(activity_id)` | Split summaries |
| `get_activity_typed_splits(activity_id)` | Typed splits |
| `get_activity_weather(activity_id)` | Weather during activity |
| `get_activity_exercise_sets(activity_id)` | Exercise sets (strength training) |
| `get_activity_hr_in_timezones(activity_id)` | Heart rate time in zones |
| `get_activity_power_in_timezones(activity_id)` | Power distribution in zones |
| `get_activity_gear(activity_id)` | Gear used for activity |
| `get_activity_types()` | All available activity types |

### Activity Management

| Tool | Description |
|------|-------------|
| `delete_activity(activity_id)` | Delete an activity |
| `set_activity_name(activity_id, title)` | Rename an activity |
| `set_activity_type(activity_id, type_id, type_key, parent_type_id)` | Change activity type |
| `download_activity(activity_id, dl_fmt)` | Download activity file (tcx, gpx, csv, kml, fit) |
| `create_manual_activity(...)` | Create a manual activity |
| `create_manual_activity_from_json(payload_json)` | Create activity from raw JSON |

### Workouts & Training

| Tool | Description |
|------|-------------|
| `get_workouts(start, limit)` | List saved workouts |
| `get_workout_by_id(workout_id)` | Get a specific workout |
| `download_workout(workout_id)` | Download a workout |
| `get_scheduled_workout_by_id(id)` | Get a scheduled workout |
| `upload_workout(workout_json)` | Create a workout from JSON |
| `upload_running_workout(workout_json)` | Create a running workout |
| `upload_cycling_workout(workout_json)` | Create a cycling workout |
| `upload_swimming_workout(workout_json)` | Create a swimming workout |
| `upload_hiking_workout(workout_json)` | Create a hiking workout |
| `upload_walking_workout(workout_json)` | Create a walking workout |
| `schedule_workout(workout_id, date_str)` | Schedule a workout on a date |

### Training Plans

| Tool | Description |
|------|-------------|
| `get_training_plans()` | List training plans (Garmin Coach) |
| `get_training_plan_by_id(plan_id)` | Get a training plan |
| `get_adaptive_training_plan_by_id(plan_id)` | Get an adaptive training plan |

### Body Composition & Weight

| Tool | Description |
|------|-------------|
| `get_body_composition(startdate, enddate)` | Body composition data |
| `get_weigh_ins(startdate, enddate)` | Weigh-in records |
| `get_daily_weigh_ins(cdate)` | Daily weigh-ins |
| `add_weigh_in(weight, unit_key)` | Add a weigh-in |
| `add_body_composition(timestamp, weight, ...)` | Add body composition data |
| `delete_weigh_in(weight_pk, cdate)` | Delete a weigh-in |
| `add_hydration_data(value_in_ml, cdate)` | Add hydration data |

### Blood Pressure

| Tool | Description |
|------|-------------|
| `get_blood_pressure(startdate, enddate)` | Get blood pressure data |
| `set_blood_pressure(systolic, diastolic, pulse)` | Record blood pressure |

### Nutrition

| Tool | Description |
|------|-------------|
| `get_nutrition_daily_food_log(cdate)` | Daily food log |
| `get_nutrition_daily_meals(cdate)` | Daily meals |
| `get_nutrition_daily_settings(cdate)` | Nutrition settings |

### Gear Tracking

| Tool | Description |
|------|-------------|
| `get_gear(user_profile_number)` | User gear (shoes, bikes, equipment) |
| `get_gear_stats(gear_uuid)` | Gear statistics (distance, activities) |
| `get_gear_activities(gear_uuid, limit)` | Activities for a gear item |
| `get_gear_defaults(user_profile_number)` | Default gear settings |
| `add_gear_to_activity(gear_uuid, activity_id)` | Add gear to activity |
| `remove_gear_from_activity(gear_uuid, activity_id)` | Remove gear from activity |

### Goals & Achievements

| Tool | Description |
|------|-------------|
| `get_personal_record()` | Personal records |
| `get_earned_badges()` | Earned badges |
| `get_available_badges()` | Available badges |
| `get_in_progress_badges()` | In-progress badges |
| `get_goals(status)` | User goals (active, future, past) |

### Challenges

| Tool | Description |
|------|-------------|
| `get_badge_challenges(start, limit)` | Badge challenges |
| `get_adhoc_challenges(start, limit)` | Ad-hoc challenges |
| `get_inprogress_virtual_challenges(start, limit)` | Virtual challenges |

### Devices

| Tool | Description |
|------|-------------|
| `get_devices()` | Connected devices |
| `get_device_last_used()` | Last used device |
| `get_device_settings(device_id)` | Device settings |
| `get_device_alarms()` | Device alarms |
| `get_device_solar_data(device_id, startdate)` | Solar data (solar devices) |
| `get_primary_training_device()` | Primary training device |

### User Profile

| Tool | Description |
|------|-------------|
| `get_user_profile()` | Profile and settings |
| `get_userprofile_settings()` | Detailed profile settings |
| `get_unit_system()` | Unit system (metric/imperial) |

### Golf

| Tool | Description |
|------|-------------|
| `get_golf_summary(start, limit)` | Golf summary |
| `get_golf_scorecard(scorecard_id)` | Golf scorecard |
| `get_golf_shot_data(scorecard_id, hole_numbers)` | Golf shot data |

### Women's Health

| Tool | Description |
|------|-------------|
| `get_menstrual_calendar_data(startdate, enddate)` | Menstrual calendar |
| `get_menstrual_data_for_date(fordate)` | Menstrual data for a date |
| `get_pregnancy_summary()` | Pregnancy summary |

## Transport Modes

| Command | Mode | Endpoint |
|---------|------|----------|
| `mcp-garmin` | stdio (default) | For Claude Desktop |
| `mcp-garmin-sse` | SSE | `http://0.0.0.0:8000/sse` |
| `mcp-garmin-http` | Streamable HTTP | `http://0.0.0.0:8000/mcp` |

Host and port can be configured via `MCP_HOST` and `MCP_PORT` environment variables (SSE mode).

## Docker

```bash
docker build -t mcp-garmin -f containers/mcp-garmin/Dockerfile .

docker run -p 8000:8000 \
  -v ~/.garminconnect:/root/.garminconnect \
  -e GARMIN_EMAIL="your-email@example.com" \
  -e GARMIN_PASSWORD="your-password" \
  mcp-garmin
```

## Kubernetes

The `mcp-garmin-init` command is interactive (requires MFA/2FA input), so authentication must be done **locally first**, then tokens are injected into the cluster as a Secret.

### 1. Generate tokens locally

```bash
pip install -e .
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"

mcp-garmin-init
# Enter your 2FA code when prompted
# Tokens are saved to ~/.garminconnect/
```

### 2. Create a Kubernetes Secret from the tokens

```bash
kubectl create secret generic garmin-tokens \
  --from-file=oauth1_token.json=$HOME/.garminconnect/oauth1_token.json \
  --from-file=oauth2_token.json=$HOME/.garminconnect/oauth2_token.json
```

### 3. Deploy

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-garmin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mcp-garmin
  template:
    metadata:
      labels:
        app: mcp-garmin
    spec:
      containers:
        - name: mcp-garmin
          image: mcp-garmin:latest
          ports:
            - containerPort: 8000
          env:
            - name: GARMINTOKENS
              value: /tokens
          volumeMounts:
            - name: garmin-tokens
              mountPath: /tokens
              readOnly: true
      volumes:
        - name: garmin-tokens
          secret:
            secretName: garmin-tokens
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-garmin
spec:
  selector:
    app: mcp-garmin
  ports:
    - port: 8000
      targetPort: 8000
```

### Token renewal

Tokens are valid for ~1 year. When they expire:

```bash
mcp-garmin-init                    # Re-authenticate locally
kubectl delete secret garmin-tokens
kubectl create secret generic garmin-tokens \
  --from-file=oauth1_token.json=$HOME/.garminconnect/oauth1_token.json \
  --from-file=oauth2_token.json=$HOME/.garminconnect/oauth2_token.json
kubectl rollout restart deployment/mcp-garmin
```

## Pre-commit

Pre-requisite:
```bash
python3 -m pip install pre-commit
# Detect-secrets
python3 -m pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

```bash
pre-commit install
```

## Enforcing conventional commit

This repo follows the angular [conventional commits](https://conventionalcommits.org/).
