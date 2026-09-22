---
name: generate
description: Pay-as-you-go AI image and video generation through kie.ai, the cheap alternative to a Higgsfield subscription. Fires on "generate a video/image", "make a clip", "kie", "cheapest way to make this video", or any request to create an AI image or short video without burning a monthly subscription. Quotes the cost first, waits for your go, runs the cheapest model that fits, saves every file to a local folder.
---

# generate — kie.ai pay-as-you-go image/video

Replaces a Higgsfield subscription. kie.ai bills per generation (1 credit = $0.005),
unused credits never expire, no monthly fee. One API key fronts Veo 3.1, Kling, Seedance,
Nano Banana, and more.

Runner: `~/.claude/skills/generate/kie.py` (Python 3, standard library only)

## One-time setup

The runner reads the key from the `KIE_API_KEY` environment variable. To get one: sign up
at kie.ai, add credits, and create a key on the API keys page. Nothing runs until that key
exists. Never paste the key into chat; set it as an environment variable yourself.
Files land in `~/kie-generations/` unless `KIE_OUT` points somewhere else.

## How to use it

Always quote before spending. Anything over ~50 credits ($0.25) needs an explicit go
first.

**1. Quote (spends nothing):**
```bash
python ~/.claude/skills/generate/kie.py quote --kind video
```

**2. Show the quote, wait for an explicit "go".** A question is not a go.

**3. Run (spends credits, needs --go):**
```bash
python ~/.claude/skills/generate/kie.py run "your prompt here" \
  --kind video --aspect 9:16 --resolution 1080p --duration 8 --go
```

Without `--go` the `run` command just prints the quote, so it is safe to dry-run.

## Choosing the model

`--model auto` (default) picks the cheapest model of that kind. Override with `--model`:

| kind  | model         | id                        | ~cost      |
|-------|---------------|---------------------------|------------|
| image | nano-banana   | google/nano-banana        | $0.02      |
| image | nano-banana-pro | google/nano-banana-pro  | $0.10      |
| video | veo-lite      | veo3_lite                 | $0.20 / 8s |
| video | veo-fast      | veo3_fast                 | $0.30 / 8s |
| video | veo           | veo3 (Veo 3.1 Quality)    | $1.60 / 8s |
| video | seedance      | bytedance/seedance-v1-pro | ~$0.45     |
| video | kling         | kling/v2-master           | ~$0.35     |

Prices are an estimate table; the run reports the ACTUAL credits kie charged. Verify
high-volume numbers at kie.ai/pricing.

## Image-to-video and edits

Pass a reference image URL (repeatable):
```bash
python ~/.claude/skills/generate/kie.py run "she turns and smiles" --kind video --model veo-fast \
  --image-url https://.../still.png --go
```
The still must be a public URL kie can fetch. For a local file, upload it somewhere
reachable first.

## The workflow Sabrina Ramonov showed (the source of this)

Draft the image first, then animate the still. So for a viral clip:
1. `run --kind image` a still with Nano Banana (~2 cents),
2. take that image URL,
3. `run --kind video --image-url <that>` to animate it.

Cheaper and more controllable than text-to-video in one shot.

## Output

Every generation lands in `~/kie-generations/<timestamp>_<slug>/` (or under `KIE_OUT`)
with the prompt, the raw response JSON, and the downloaded media.

## Guardrails

- Quote first, wait for a go on anything past a couple cents.
- If a jobs-API model id or price looks stale (kie changes them), check docs.kie.ai/market
  and update the `MODELS` table in kie.py rather than guessing.
