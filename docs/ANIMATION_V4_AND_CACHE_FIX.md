# StudentBridge AI V4 — Visible Animations and Fixing the Old Page

## What moves?

1. The globe-style rings turn continuously, with visible glowing dots.
2. Three lights travel along country-to-country paths.
3. Country flags gently float.
4. The **Explore a country pair** preview switches every 4.3 seconds and a progress bar advances.
5. **Pause/Play** controls the visual animation. **Use this pair** opens the payment planner with the selected origin/destination.

These visuals show supported planning country pairs. They are NOT live remittance executions or current bank quotes.

## Why might you still see the old homepage?

The old page has an **Explore verified data** button. V4 says **Ask Bridge AI** and the top right says **DEMO MODE · V4**. If the latter are missing, the old page/server is still running, or your Chrome cache is stale.

1. In the Terminal running the OLD StudentBridge server, press `Ctrl+C`.
2. To check for other servers on the same port, on Mac run `lsof -nP -iTCP:8000 -sTCP:LISTEN`. If a server remains, stop its own Terminal process. Only use `kill <PID>` on a PID you identify as your old StudentBridge server.
3. Extract the new V4 zip into its own folder. Copy `.env` from your already-working MySQL folder. Do not share it.
4. From the **new V4 folder** run:

    ```bash
    source .venv/bin/activate
    python scripts/check_mysql.py
    python run.py
    ```

    If `.venv` does not exist yet, run `python3 -m venv .venv` and `python -m pip install -r requirements.txt` after activating it.

5. Open `http://127.0.0.1:8000/?v=4` and use `Cmd+Shift+R` to force reload on Mac Chrome. The CSS and JS also use a version string to bypass old asset caching.
6. In the homepage, look for the **Explore a country pair** box at the bottom of the large dark hero panel, changing from **China → Australia** to **Japan → United Kingdom**.

## If nothing moves

In macOS **System Settings > Accessibility > Display**, check **Reduce motion**. When that setting is on, the project honors it by stopping the automatic motion by default. The Pause/Play button lets you start it manually.

No MySQL migration or additional SQL statements are needed for this visual update.
