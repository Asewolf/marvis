---
name: feedback-example
description: Example of a correction turned permanent. Delete once you have real ones
metadata:
  type: feedback
---

State the rule plainly. "Never modify a test to make it pass. Fix the code or ask me."

**Why:** A passing test suite that was edited into passing is worse than a failing one,
because it hides the break and I stop trusting the suite.

**How to apply:** If a test fails, the test is reporting something. Fix the code. If the
test is genuinely wrong, say so and wait rather than editing it.

Related: [[user-profile]]
