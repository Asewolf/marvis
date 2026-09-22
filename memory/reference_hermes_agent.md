---
name: hermes-agent
description: Hermes Agent setup and model choice, for uncensored local file editing
metadata:
  type: reference
---

Nous Research's agent harness. Tool calling plus file access, paired with a lightly
aligned model. Used for editing game files without a policy layer in the way.

**Docs:** https://hermes-agent.nousresearch.com/docs/
**Repo:** https://github.com/nousresearch/hermes-agent
**Install guide:** https://hermesatlas.com/guide/install/

## Requirements

Python 3.11+, on Linux, macOS, or Windows via WSL2. Not native Windows. No Docker needed
for the official installer. Install runs in about two minutes.

## Setup

```bash
hermes setup --portal   # OAuth, covers a model plus web search, images, TTS, browser
hermes model            # pick the LLM
hermes tools            # pick which tools are enabled
```

## Model choice

**Hosted:** Hermes 4 405B is the strongest in the line. Llama 3.1 405B base, hybrid
reasoning. Too large to run at home, so use the Nous Portal subscription or OpenRouter
(https://openrouter.ai/nousresearch/hermes-4-405b).

**Local:** Hermes 4.3 36B on a 24GB GPU. Smaller, but no API dependency.

**Minimum context is 64k.** Below that the agent loses the thread across multi-step tool
calls.

## Operating notes

Point it at the specific game folder, never the whole drive. It writes files, and a
lightly aligned 405B is not a cautious one.

Back up saves before the first run.

Related: [[user-profile]]
