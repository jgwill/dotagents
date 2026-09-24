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

## Local-image attachment in an existing Page post

Verified 2026-09-24: open the exact permalink → Actions → Edit post → Photo/video. Inspect the edit dialog's `input[type=file]` elements: the media input may be hidden and absent from accessibility snapshots. `browser_cdp` is stateless here, so a `Runtime.evaluate` `objectId` cannot be reused in a later `DOM.setFileInputFiles` call. Use **one** stateful connection to the already-running local Chrome tab, after confirming the file and post target:

```python
import asyncio, json, requests, websockets

async def attach(local_image, post_url_fragment, file_input_index):
    tabs = requests.get('http://127.0.0.1:9222/json/list', timeout=5).json()
    tab = next(t for t in tabs if t.get('type') == 'page' and post_url_fragment in t.get('url', ''))
    async with websockets.connect(tab['webSocketDebuggerUrl'], origin=None, max_size=2**21) as ws:
        async def rpc(i, method, params):
            await ws.send(json.dumps({'id': i, 'method': method, 'params': params}))
            while True:
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=15))
                if msg.get('id') == i:
                    if 'error' in msg: raise RuntimeError(msg['error'])
                    return msg['result']
        expr = f'document.querySelectorAll(\'[role="dialog"] input[type="file"]\')[{file_input_index}]'
        result = await rpc(1, 'Runtime.evaluate', {'expression': expr, 'returnByValue': False})
        await rpc(2, 'DOM.setFileInputFiles', {'files': [local_image], 'objectId': result['result']['objectId']})

# asyncio.run(attach('/absolute/approved-image.jpg', '/Guillaumecoder/posts/<id>', 1))
```

The example index `1` matched the multiple-image input in one Edit post dialog; inspect `accept` and `multiple` before every use rather than assuming fixed indices. Verify the media preview and unchanged text, then Next → check Page, Public, Boost off, and AI label as appropriate → Save. Reload the **same permalink** and inspect the rendered image and text. CDP must remain bound to loopback; never read cookies/tokens.

## User handoff

1. Open the dedicated Chrome window.
2. The user signs in and completes CAPTCHA/2FA directly.
3. The user opens the intended Page.
4. Hermes lists targets and inspects only that Page tab.
5. Keep Chrome open while drafting/publishing.

Never copy the regular Chrome profile into the dedicated directory. Never bind the debug endpoint to `0.0.0.0`.

## Telegram limitation

`/browser connect` is an interactive Hermes CLI command, not a Telegram gateway command. For gateway sessions, use persistent `browser.cdp_url` configuration or `BROWSER_CDP_URL` in the gateway environment, then verify the endpoint before using browser tools.
