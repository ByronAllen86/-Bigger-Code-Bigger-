# App Factory Generator

`generate_app_factory.sh` generates 20 subscription-first Android app
projects (Kotlin / Jetpack Compose, clean architecture, Google Play
Billing 7 paywalls) into `App_Factory_Output/Android_Apps/` on your
Desktop. It is fully unattended - no prompts, no network access needed.

## Running it on Windows

1. Open **Git Bash** (installed with Git for Windows).
2. Clone this repo (or just download `generate_app_factory.sh`).
3. Run:

   ```bash
   bash generate_app_factory.sh
   ```

The script auto-detects your Windows Desktop (it also works under WSL,
Linux, and macOS). Expect 20 project folders and ~320 files.

## After generation

Open any app folder in **Android Studio** (File > Open). The first sync
downloads Gradle 8.9 and all dependencies automatically, then the app
runs on an emulator or device. See `App_Factory_Output/README.md`
(generated) for the full portfolio list and the Play Console steps to
wire up live subscription pricing.
