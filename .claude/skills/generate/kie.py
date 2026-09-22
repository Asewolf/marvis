#!/usr/bin/env python3
"""
kie.py - pay-as-you-go image/video generation through kie.ai.

Replaces a Higgsfield subscription. kie.ai charges per generation (1 credit =
$0.005), unused credits never expire. This runner does three things:

  quote     estimate the cost BEFORE spending anything
  run       submit the cheapest model that fits, poll, download to a folder
  cheapest  print the cheapest model for a given kind

The key comes from the KIE_API_KEY environment variable. Nothing runs without it.

Prices below are a table, not a live feed - kie.ai/pricing 403s to scripts and
model prices move. Each run also reports the ACTUAL credits kie charged, so the
table is only used for the up-front quote. Verify big jobs at kie.ai/pricing.
# ponytail: hardcoded price table; the poll response carries real credits spent,
# so drift only affects the estimate, never the accounting.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error, re
from datetime import datetime

OUT_ROOT = os.environ.get("KIE_OUT") or os.path.join(os.path.expanduser("~"), "kie-generations")
BASE = "https://api.kie.ai"

USD_PER_CREDIT = 0.005

# kind: image | video
# family: "veo" (dedicated /veo endpoints) | "jobs" (/jobs/createTask)
# usd: estimated cost for the default unit (image = 1 image; video = per the note)
MODELS = {
    # ---- images (jobs API) ----
    "nano-banana":      {"kind": "image", "family": "jobs", "id": "google/nano-banana",     "usd": 0.02,  "note": "1 image"},
    "nano-banana-pro":  {"kind": "image", "family": "jobs", "id": "google/nano-banana-pro", "usd": 0.10,  "note": "1 image"},
    "nano-banana-2":    {"kind": "image", "family": "jobs", "id": "nano-banana-2",          "usd": 0.10,  "note": "1 image"},
    # ---- video (Veo dedicated endpoints) ----
    "veo-lite":  {"kind": "video", "family": "veo", "id": "veo3_lite", "usd": 0.20, "note": "8s 720p"},
    "veo-fast":  {"kind": "video", "family": "veo", "id": "veo3_fast", "usd": 0.30, "note": "8s 720p"},
    "veo":       {"kind": "video", "family": "veo", "id": "veo3",      "usd": 1.60, "note": "8s 1080p"},
    # ---- video (jobs API) - ids/prices per kie market, verify before high volume ----
    "seedance":  {"kind": "video", "family": "jobs", "id": "bytedance/seedance-v1-pro",  "usd": 0.45, "note": "5s 1080p (verify)"},
    "kling":     {"kind": "video", "family": "jobs", "id": "kling/v2-master",            "usd": 0.35, "note": "5s (verify)"},
}


def load_key():
    k = os.environ.get("KIE_API_KEY")
    if not k:
        sys.exit("KIE_API_KEY is not set. Get a key at kie.ai "
                 "(sign up, add credits, API keys) and set it as an environment variable.")
    return k


def _req(method, path, key, body=None, timeout=60):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + key)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        sys.exit(f"kie {method} {path} -> HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"kie {method} {path} -> {e.reason}")


def cheapest(kind):
    cands = {n: m for n, m in MODELS.items() if m["kind"] == kind}
    if not cands:
        sys.exit(f"no models of kind '{kind}'")
    return min(cands.items(), key=lambda kv: kv[1]["usd"])


def quote(model_name, kind):
    if model_name == "auto":
        name, m = cheapest(kind)
    else:
        m = MODELS.get(model_name)
        if not m:
            sys.exit(f"unknown model '{model_name}'. Known: {', '.join(MODELS)}")
        name = model_name
    print(f"model:    {name}  ({m['id']})")
    print(f"kind:     {m['kind']}")
    print(f"estimate: ~${m['usd']:.2f}  ({m['note']})")
    print(f"          ~{int(m['usd']/USD_PER_CREDIT)} credits @ ${USD_PER_CREDIT}/credit")
    print("note:     estimate only. Actual credits are reported after the run.")
    return name, m


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "gen").lower()).strip("-")[:40] or "gen"


def _outdir(prompt):
    d = os.path.join(OUT_ROOT, datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + _slug(prompt))
    os.makedirs(d, exist_ok=True)
    return d


def _download(urls, outdir):
    saved = []
    for i, u in enumerate(urls):
        ext = os.path.splitext(u.split("?")[0])[1] or (".mp4" if "video" in u else ".png")
        p = os.path.join(outdir, f"out_{i}{ext}")
        try:
            urllib.request.urlretrieve(u, p)
            saved.append(p)
        except Exception as e:
            print(f"  download failed for {u}: {e}")
    return saved


def _submit(m, key, prompt, image_urls, aspect, resolution, duration):
    if m["family"] == "veo":
        gtype = "REFERENCE_2_VIDEO" if image_urls else "TEXT_2_VIDEO"
        body = {"prompt": prompt, "model": m["id"], "generationType": gtype,
                "aspect_ratio": aspect, "resolution": resolution, "duration": duration}
        if image_urls:
            body["imageUrls"] = image_urls
        r = _req("POST", "/api/v1/veo/generate", key, body)
        tid = (r.get("data") or {}).get("taskId")
        return tid, "veo"
    else:
        inp = {"prompt": prompt}
        if m["kind"] == "image":
            inp["output_format"] = "png"
            inp["aspect_ratio"] = aspect
        else:
            inp["aspect_ratio"] = aspect
            inp["resolution"] = resolution
            inp["duration"] = duration
        if image_urls:
            inp["image_urls"] = image_urls
        body = {"model": m["id"], "input": inp}
        r = _req("POST", "/api/v1/jobs/createTask", key, body)
        tid = (r.get("data") or {}).get("taskId")
        return tid, "jobs"


def _poll(family, tid, key, timeout_s=600):
    start = time.time()
    while time.time() - start < timeout_s:
        if family == "veo":
            r = _req("GET", f"/api/v1/veo/record-info?taskId={tid}", key)
            d = r.get("data") or {}
            flag = d.get("successFlag")
            if flag == 1:
                resp = d.get("response") or {}
                urls = resp.get("fullResultUrls") or resp.get("resultUrls") or []
                return urls, d
            if flag in (2, 3):
                sys.exit(f"generation failed (successFlag={flag}): {json.dumps(d)[:400]}")
        else:
            r = _req("GET", f"/api/v1/jobs/recordInfo?taskId={tid}", key)
            d = r.get("data") or {}
            state = (d.get("state") or d.get("status") or "").lower()
            if state in ("success", "completed", "succeeded"):
                rj = d.get("resultJson") or "{}"
                try:
                    urls = (json.loads(rj) if isinstance(rj, str) else rj).get("resultUrls") or []
                except Exception:
                    urls = []
                return urls, d
            if state in ("failed", "error"):
                sys.exit(f"generation failed: {json.dumps(d)[:400]}")
        print("  ...working")
        time.sleep(8)
    sys.exit(f"timed out after {timeout_s}s waiting on task {tid}")


def _credits_spent(meta):
    for k in ("costCredits", "creditsUsed", "credits", "consumeCredits"):
        v = meta.get(k)
        if isinstance(v, (int, float)):
            return v
    return None


def run(model_name, kind, prompt, image_urls, aspect, resolution, duration):
    key = load_key()
    name, m = quote(model_name, kind)
    print()
    outdir = _outdir(prompt)
    open(os.path.join(outdir, "prompt.txt"), "w", encoding="utf-8").write(prompt or "")
    print(f"submitting to {m['id']} ...")
    tid, family = _submit(m, key, prompt, image_urls, aspect, resolution, duration)
    if not tid:
        sys.exit("no taskId returned - check the request against docs.kie.ai")
    print(f"taskId: {tid}  (folder: {outdir})")
    urls, meta = _poll(family, tid, key)
    json.dump(meta, open(os.path.join(outdir, "response.json"), "w", encoding="utf-8"), indent=2)
    if not urls:
        sys.exit("finished but no result URLs in the response - see response.json")
    saved = _download(urls, outdir)
    spent = _credits_spent(meta)
    print("\nDONE.")
    for p in saved:
        print("  " + p)
    if spent is not None:
        print(f"  charged: {spent} credits (~${spent*USD_PER_CREDIT:.2f})")
    return saved


def _selfcheck():
    # cheapest of each kind resolves and the table is internally consistent
    for kind in ("image", "video"):
        n, m = cheapest(kind)
        assert m["kind"] == kind, (kind, n)
    for n, m in MODELS.items():
        assert m["kind"] in ("image", "video"), n
        assert m["family"] in ("veo", "jobs"), n
        assert m["usd"] > 0, n
    assert cheapest("image")[0] == "nano-banana"      # cheapest image today
    assert cheapest("video")[0] == "veo-lite"          # cheapest video today
    print("selfcheck OK")


def main():
    ap = argparse.ArgumentParser(description="kie.ai pay-as-you-go generation")
    sub = ap.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("quote", help="estimate cost, spend nothing")
    q.add_argument("--kind", choices=["image", "video"], default="video")
    q.add_argument("--model", default="auto")

    c = sub.add_parser("cheapest", help="print the cheapest model for a kind")
    c.add_argument("--kind", choices=["image", "video"], default="video")

    r = sub.add_parser("run", help="generate (spends credits)")
    r.add_argument("prompt")
    r.add_argument("--kind", choices=["image", "video"], default="video")
    r.add_argument("--model", default="auto", help="auto = cheapest that fits")
    r.add_argument("--image-url", action="append", dest="image_urls", default=[],
                   help="reference image URL (repeatable, for image-to-video / edit)")
    r.add_argument("--aspect", default="9:16")
    r.add_argument("--resolution", default="1080p", choices=["720p", "1080p", "4k"])
    r.add_argument("--duration", type=int, default=8, choices=[4, 6, 8])
    r.add_argument("--go", action="store_true", help="required to actually spend credits")

    sub.add_parser("selfcheck")

    a = ap.parse_args()
    if a.cmd == "quote":
        quote(a.model, a.kind)
    elif a.cmd == "cheapest":
        n, m = cheapest(a.kind)
        print(f"{n}  ({m['id']})  ~${m['usd']:.2f}  {m['note']}")
    elif a.cmd == "selfcheck":
        _selfcheck()
    elif a.cmd == "run":
        if not a.go:
            print("DRY RUN. This is the quote. Add --go to actually generate.\n")
            quote(a.model, a.kind)
            return
        run(a.model, a.kind, a.prompt, a.image_urls, a.aspect, a.resolution, a.duration)


if __name__ == "__main__":
    main()
