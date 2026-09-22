---
name: post-grader
description: Maker≠checker quality gate for social posts BEFORE they ship. Fires on "grade this post", "is this caption good", "rate this draft", "check this before it posts", and as the final QA step for any automated social post or outreach post. Input = post text (or file path) + platform. Output = score/10 scorecard, pass/fail voice audit, top 3 ranked fixes. Below 7/10 = do not auto-post.
---

# Post Grader

Grade a social post for performance before it ships. Harsh but fair: a false 8 wastes more
time than an honest 5. This is the CHECKER half of maker≠checker. Never grade a post in the
same breath you wrote it; grade as a fresh critical pass (or a separate agent for autopilot).

## Rubric (7 dimensions, weighted)

| Dimension | Weight | What scores high |
|---|---|---|
| Hook strength | 50% | First 3-5 words arrest attention: specific, surprising, emotional, or polarizing. Throat-clearing = instant low score. Test: would the first line work as a standalone tweet? |
| Curiosity + specificity | 10% | Real numbers/names/moments, not generic claims; opens tension that the post resolves |
| Emotional charge | 10% | Provokes surprise, anger, vindication, recognition, or pride |
| Share-worthiness | 10% | Reader would tag, screenshot, save, or forward it |
| Voice match | 10% | Matches the sender's actual voice (see per-pipeline voices below); zero generic-AI tone |
| Polarity | 5% | Takeable position: reader can nod hard or push back |
| Platform fit | 5% | Length, hook placement, hashtag count, format native to the platform |

Score each 1-10. Overall = weighted average minus voice-audit penalties (−0.5 per failed
rule, capped −3). 7 = good, 8 = strong, 9 = near-perfect, 10 doesn't exist. Most hooks
honestly score 4-6. If the hook is weak, rewrite it first (hook = half the score, so that's
always fix #1).

## Voice audit (pass/fail each)

1. Zero em dashes anywhere
2. Contractions ("don't", not "do not")
3. Digits, not spelled-out numbers ("5 tips")
4. Active voice: no "was created" / "is being done"
5. No filler words: really, very, just, basically, literally, actually, simply
6. No filler openers: "in today's world", "let me tell you", "the truth is", "here's the thing"
7. Hashtags: 0 on X/Threads/Bluesky/LinkedIn/Facebook; 3-5 on Instagram; max 5 on TikTok

Edit these seven to match your own writing rules. They're the part most worth personalizing.

## Per-pipeline voice (what "voice match" means)

Write one line per account or pipeline you post from. Examples:

- **Persona or character accounts:** casual, like texting a friend. Lowercase fine, typos
  fine, short. A polished marketing hook FAILS voice match even if it scores 10 on hook
  strength, because the realism is the product.
- **Business outreach:** plain language, no dashes, no bold links, spell things out, one
  clear ask.
- **Your own accounts:** direct, casual, first person, no corporate tone.

## Workflow

1. Get the post (inline text or Read the file) + target platform.
2. Score the 7 dimensions; one-line note for anything under 8.
3. Run the 7 voice rules; list violations.
4. Compute overall; output a compact scorecard table.
5. Top 3 fixes ranked by impact, each with the exact current quote, one line on why it
   hurts, and a specific rewrite. Do NOT rewrite the whole post; fix instructions only.
6. Autopilot integration: below 7/10 = post is blocked, gets fixed and regraded before
   scheduling. Interactive: hand over the scorecard, offer to apply the fixes.

## Gotchas

- Don't pad scores and don't flag style preferences as errors. Judge only against the
  rubric and the 7 rules.
- Grader ≠ writer. If you just drafted the post, grade it as a hostile stranger seeing only
  the final text, or spawn a separate agent for the grade.
- Persona-post exception on rule polish: authentic-messy beats optimized-clean. When rubric
  polish and persona realism conflict, realism wins; say so in the scorecard.
