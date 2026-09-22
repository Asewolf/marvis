"""Open a URL via CDP, scroll down in steps, screenshot each viewport.
Usage: python cdp_scroll_cap.py <port> <url> <out_prefix> <n_scrolls> <scroll_px>"""
import asyncio, json, sys, base64, urllib.request
import websockets

PORT, URL, PREFIX = sys.argv[1], sys.argv[2], sys.argv[3]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 3
STEP = int(sys.argv[5]) if len(sys.argv) > 5 else 2200


def http_json(path):
    return json.load(urllib.request.urlopen(f"http://localhost:{PORT}{path}", timeout=10))


async def call(ws, _id, method, params=None):
    await ws.send(json.dumps({"id": _id, "method": method, "params": params or {}}))
    while True:
        m = json.loads(await ws.recv())
        if m.get("id") == _id:
            return m


async def main():
    bws = http_json("/json/version")["webSocketDebuggerUrl"]
    async with websockets.connect(bws, max_size=None) as b:
        r = await call(b, 1, "Target.createTarget", {"url": URL})
        tid = r["result"]["targetId"]

    page_ws = None
    for _ in range(30):
        for t in http_json("/json"):
            if t.get("id") == tid and t.get("webSocketDebuggerUrl"):
                page_ws = t["webSocketDebuggerUrl"]; break
        if page_ws: break
        await asyncio.sleep(0.5)
    if not page_ws:
        print("ERROR: no attach"); return

    async with websockets.connect(page_ws, max_size=None) as ws:
        await call(ws, 10, "Page.enable")
        await call(ws, 11, "Runtime.enable")
        await asyncio.sleep(8)
        _id = 100
        for i in range(N):
            shot = (await call(ws, _id, "Page.captureScreenshot",
                               {"format": "png", "captureBeyondViewport": False}))["result"]["data"]
            with open(f"{PREFIX}_{i}.png", "wb") as f:
                f.write(base64.b64decode(shot))
            print("wrote", f"{PREFIX}_{i}.png")
            _id += 1
            await call(ws, _id, "Runtime.evaluate", {"expression": f"window.scrollBy(0,{STEP})"})
            _id += 1
            await asyncio.sleep(2.5)
        try:
            await call(ws, 999, "Page.close")
        except Exception:
            pass


asyncio.run(main())
