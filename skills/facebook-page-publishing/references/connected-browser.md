# Connected Facebook Browser

## Verified local setup

Measured on 2026-09-23 on `/home/mia`:

- Browser: Google Chrome 153
- CDP protocol: 1.3
- Endpoint: `http://127.0.0.1:9222`
- Dedicated user data: `/home/mia/.hermes/chrome-debug`
- Desktop: KDE/X11 display `:0`
- Hermes config: `browser.cdp_url: http://127.0.0.1:9222`

Launch from the interactive KDE desktop:

```bash
/usr/bin/google-chrome \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/mia/.hermes/chrome-debug \
  --no-first-run \
  --no-default-browser-check \
  https://www.facebook.com/
```

If launching from the Hermes gateway service, supply the desktop environment:

```bash
DISPLAY=:0 \
XAUTHORITY=/home/mia/.Xauthority \
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1007/bus \
XDG_RUNTIME_DIR=/run/user/1007 \
/usr/bin/google-chrome \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/mia/.hermes/chrome-debug \
  --no-first-run \
  --no-default-browser-check \
  https://www.facebook.com/
```

Verify without exposing cookie or credential data:

```bash
python3 - <<'PY'
import json, urllib.request
with urllib.request.urlopen('http://127.0.0.1:9222/json/version', timeout=2) as r:
    data = json.load(r)
print(data.get('Browser'))
print(data.get('Protocol-Version'))
PY
```

## User handoff

1. Open the dedicated Chrome window.
2. The user signs in and completes CAPTCHA/2FA directly.
3. The user opens the intended Page.
4. Hermes lists targets and inspects only that Page tab.
5. Keep Chrome open while drafting/publishing.

Never copy the regular Chrome profile into the dedicated directory. Never bind the debug endpoint to `0.0.0.0`.

## Telegram limitation

`/browser connect` is an interactive Hermes CLI command, not a Telegram gateway command. For gateway sessions, use persistent `browser.cdp_url` configuration or `BROWSER_CDP_URL` in the gateway environment, then verify the endpoint before using browser tools.
