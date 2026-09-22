# The skill set

Three skills in this repo are ours, under `.claude/skills/`. The rest of the working set
comes from other people, and this page is the map: who wrote each one, what it's licensed
under, and the author's own install command.

Nothing third-party is copied into this repo. You install from the author, so they keep the
credit and the download, and you get their current version instead of a stale snapshot.

Skills live in `~/.claude/skills/`. Claude Code reads them on the next session start.

## In this repo

| Skill | What it does |
|---|---|
| `read-walled-links` | Reads and watches links behind a login, and pulls full transcripts out of long videos. See [browser-automation.md](browser-automation.md). |
| `post-grader` | Scores a social post before it ships, on hook strength and voice. Below 7 out of 10, it doesn't post. |
| `generate` | Pay-as-you-go image and video generation through kie.ai. Quotes the cost first and waits for a go before spending. |

## From other authors

Anything below is theirs. Read each repo's license before you redistribute any of it.

### Bundles

| Bundle | Skills | Author | License | Install |
|---|---|---|---|---|
| [claude-flow / ruflo](https://github.com/ruvnet/ruflo) | 30, including swarm orchestration, SPARC, the GitHub set, AgentDB and the v3 series | ruvnet | MIT | `npx ruflo@latest init` |
| [hyperframes](https://github.com/heygen-com/hyperframes) | 21, video composition: animation, captions, music videos, talking-head recuts, product launch videos | heygen-com | Apache-2.0 | `npx hyperframes skills update`, or `npx skills add heygen-com/hyperframes --all` |
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | 13 design and frontend skills: the taste skills, brutalist and minimalist UI, image-to-code, brandkit | Leonxlnx | MIT | `npx skills add https://github.com/Leonxlnx/taste-skill` |
| [higgsfield-claude-skills](https://github.com/AKCodez/higgsfield-claude-skills) | 19 for Higgsfield and Seedance: 15 prompt-writing skills plus 4 browser automations | 15 prompt skills by [beshuaxian](https://github.com/beshuaxian/higgsfield-seedance2-jineng), 4 automations by AKCodez | none declared | Clone the repo and copy the folders into `~/.claude/skills/`, then `claude mcp add playwright npx @playwright/mcp@latest` |

`npx ruflo@latest init` sets up the whole claude-flow system in the current project, not
only the skills. Run it in a project folder you don't mind it writing to.

The Higgsfield repos carry no license file, so you can install from the author, but nobody
has permission to redistribute those files.

### Single skills

| Skill | Author | License | Install |
|---|---|---|---|
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | nextlevelbuilder | MIT | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` then `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` |
| [app-store-review](https://github.com/safaiyeh/app-store-review-skill) | safaiyeh | MIT | `/plugin marketplace add safaiyeh/app-store-review-skill` then `/plugin install app-store-review@app-store-review` |
| [img2threejs](https://github.com/img2threejs/img2threejs) | img2threejs | Apache-2.0 | `git clone https://github.com/img2threejs/img2threejs.git ~/.claude/skills/img2threejs` |
| [use-railway](https://github.com/railwayapp/railway-skills) | Railway | MIT | `/plugin marketplace add railwayapp/railway-skills` then `/plugin install railway@railway-skills` |
| [brag](https://github.com/latent-spaces/brag) | Shunit Haviv Hakimi | MIT | `/plugin marketplace add latent-spaces/brag` then `/plugin install brag@brag` |
| [scroll-craft](https://github.com/nateherkai/scroll-craft) | Nate Herk | MIT | `/plugin marketplace add nateherkai/scroll-craft` then `/plugin install nateherk-design` |
| [viral-hooks](https://github.com/Blotato-Inc/blotato-skills) | Blotato | none declared | `/plugin marketplace add Blotato-Inc/blotato-skills` then `/plugin install blotato@blotato-skills` |

The `/plugin` commands run inside Claude Code, not in a terminal.

## Two you can't install from here

- **looki-memory** reads a Looki personal-memory device. Without the device it has nothing
  to read. `clawhub install looki-memory`.
- **synced** is an Anthropic skill that arrives through your own claude.ai account. It
  appears by itself and can't be installed from a repo.

## Before you install anything

A skill is instructions an AI will follow, and sometimes code it will run. NVIDIA scanned
31,132 public skills and found vulnerabilities in 26% of them, with about 5% showing signs
of outright malicious intent. So:

- Download to a staging folder first, not straight into `~/.claude/skills/`.
- A skill that is only Markdown can't do anything until the assistant acts on its text. One
  that ships `.py`, `.sh`, `.js` or `.ps1` deserves a read of those files first.
- What's worth stopping for: code that writes into `~/.claude/`, network calls to hosts the
  skill has no reason to contact, encoded blobs that decode into more code, and any request
  to read your credentials or environment files from code rather than prose.
- Automated scanners score a skill that *discusses* security the same as one that *performs*
  an attack, so treat a scanner's findings as a list of lines to go read, never as a verdict.
