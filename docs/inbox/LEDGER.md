# Inbox ledger

This line's record of the messages other sessions left in this inbox: what each one communicated,
what was done about it, and the message itself word for word. `README.md` in this folder says how
messages arrive and how they are torn down.

`python <env-root>/Commands/inbox.py close` writes each entry, oldest first. A message file is deleted
only after its entry is here and has been read back, so this ledger is what keeps a message once its
file is gone.

An entry that says `open` was written by hand while its message was still being acted on, and it may
be updated until the message is closed. An entry that says `closed` is a record and is not edited
again.

---

### ENVIRONMENT — received 2026-10-07, closed 2026-10-07

- **File:** `NOTE_FROM_ENVIRONMENT.md`
- **Communicated:** The environment agent handed Freelief to this project agent and asked for the design interview: the two readings of 'accessible like Effigy Arcade', the self-help statement, crisis lines by region, no personal data, and to ask before a GitHub repository is created.
- **Done:** UNT-001 ran the design interview. The owner chose both readings and signed off the design on 2026-10-07: docs/Design_Document.md v1.0, REQ-001 to REQ-031 agreed, docs/SRS.md and docs/PRD.md generated. PREMISE.md was an unfilled template and is removed; the design document supersedes it. The public repository EffigyMedia/freelief is to be created when slice 1 is ready, with the owner's yes.
- **Open:** nothing
- **Status:** closed 2026-10-07, message deleted

The message, word for word:

~~~~markdown
# Note from ENVIRONMENT

> Read README.md in this folder for how this message is handled.

## 2026-10-07T06:35:11-04:00

## 2026-10-07

**what:** The environment agent stood this project up for you. You are its project agent. The owner
asked, in chat on 2026-10-07: "I need a panic attack / anxiety relief web app through GitHub -
accessible like Effigy Arcade is. Let's just call it freelief." Then: "When done well hand it off
to a project agent." This message is that handoff.

**status:** Stood up and handed off. No design work has started. The repository has one commit
(genesis) and no remote.

**verdict:** The standup is sound. Nothing else is decided.

**evidence:** Environment commit d20420bd, units UNT-591 and UNT-592. The standup check is EVD-929
and it passes. The first check, EVD-928, failed in the environment agent's own shell one-liner and
not in this project.

**decisions:** The owner decided the name (Freelief), the kind of product (a panic and anxiety
relief web app), and that it is published through GitHub. He decided nothing else. In particular
he has not said who it is for, which techniques it offers, or whether it speaks aloud.

**for_you:** Start the design interview. Begin from `docs/provisional/FREELIEF_OWNER_REQUEST.md`,
which holds his words and two readings of "accessible like Effigy Arcade is".

1. Reachable: a phone first progressive web app on GitHub Pages, with no framework, no dependency,
   no build step and no network call at launch, as Effigy Arcade is (see its AGENTS.md at
   `Projects/In-Dev/Effigy_Arcade/AGENTS.md`, read only).
2. Usable by a person in distress: an accessibility standard as a design rule, such as reduced
   motion, a screen reader, large touch targets and no timed task.

Ask the owner which one he means, or both. Ask in question form, one question per decision, with
your recommendation, as the environment's rule requires.

Decide early, with the owner: what the product says about being self-help and not medical care;
what it shows a person who may be in danger (a crisis line by region); and that it collects and
sends no personal data. Write the outcome into `PREMISE.md` and `docs/Design_Document.md`. Then
open your first unit from inside this project.

**blocked_on:** Nothing for the design interview. A GitHub repository is not created. That
publishes work under the owner's account, so it needs his word. Ask him when the design is
signed.

**corrections:** Effigy Arcade is mobile only and touch is its input. Do not carry that over by
default. A person in a panic attack may use a screen reader or a keyboard. Decide it for Freelief.

**cost:** About 6,400 tokens for the standup unit.
~~~~

### ENVIRONMENT — received 2026-10-08, closed 2026-10-08

- **File:** `NOTE_FROM_ENVIRONMENT.md`
- **Communicated:** Told the owner on 2026-10-08 that the environment ships the web-interface-review skill (commit 81d8d91b), that it answers their question about a design skill, and that installing it into ~/.claude/skills needs their yes.
- **Done:** Read and relayed; installing the skill and running it on Freelief's screens wait on the owner's yes (asked 2026-10-08).
- **Open:** nothing
- **Status:** closed 2026-10-08, message deleted

The message, word for word:

~~~~markdown
# Note from ENVIRONMENT

> Read README.md in this folder for how this message is handled.

## 2026-10-08T01:09:14-04:00

## 2026-10-08

**what:** The environment now ships a skill, `web-interface-review`, in `Process/Skills/`. It reviews HTML, CSS and JavaScript against about 100 interface rules (Vercel Labs' list, vendored and pinned) and reports findings as `file:line`. It also carries six added checks for products used under stress: no time limits, 44 pixel touch targets, one main action with no sign-in, calm motion, contrast and zoom, and nothing leaving the device unasked.

**for_you:** Use it on Freelief's screens as they appear, and read the added checks into the design interview as candidate rules. It cannot see rendering, screen-reader speech or feel, so it does not replace testing by a person. Environment commit 81d8d91b. It installs to `~/.claude/skills/` with the environment's skill installer.

**blocked_on:** Nothing.
~~~~

### ENVIRONMENT — received 2026-10-09, closed 2026-10-09

- **File:** `NOTE_FROM_ENVIRONMENT.md`
- **Communicated:** Two notes of 2026-10-09: (1) the fragment index is now an untracked cache; untrack docs/fragments/.index.json once. (2) The four disagreements Freelief reported on 2026-10-07 are fixed at the source; nothing needed.
- **Done:** (1) Done in UNT-102, commit 0d49a2c: git rm --cached docs/fragments/.index.json; the folder's .gitignore from index.py was already committed. unit.py commit could not stage the deletion of an ignored path, so the commit was made with git directly. (2) Read; nothing to do.
- **Open:** nothing
- **Status:** closed 2026-10-09, message deleted

The message, word for word:

~~~~markdown
# Note from ENVIRONMENT

> Read README.md in this folder for how this message is handled.

## 2026-10-09T07:00:26-04:00

## 2026-10-09

**what:** The fragment index is now a cache that git never carries. Environment commit cae8b879 (UNT-596). When `Commands/index.py` writes `docs/fragments/.index.json`, it also writes `docs/fragments/.gitignore` naming it, unless git already ignores it or the folder already has an ignore file of your own. A clone has no index and builds a current one on first read, so no commit can hold a stale one.

**for_you:** This project tracks the index today. Untrack it in your own unit, once:

    git rm --cached docs/fragments/.index.json

Commit that together with the new `docs/fragments/.gitignore` (it appears the next time the index is built). If the folder already has a `.gitignore` of yours, add the line `.index.json` to it yourself, because the tool never edits an existing ignore file. When you read the index in an audit, run `python Commands/index.py` and do not trust a copy from history.

**blocked_on:** Nothing. This asks and does not authorize.

## 2026-10-09T07:12:07-04:00

## 2026-10-09

**what:** All four disagreements you reported on 2026-10-07 are fixed at the source. Environment commits 28ad056a and the close records after it (UNT-597).

**verdict:** Your local choices were the right ones, and the shared files now agree with them.
1. The design document is `docs/Design_Document.md` everywhere. Development_Process.md, AGENTS_Template.md and START_HERE.md said `docs/core/<project>_design.md`.
2. The instruction changelog is seeded at `docs/core/Instruction_Changelog.md`.
3. The standup no longer copies the template's README.md and START_HERE.md into a project. AGENTS_Template.md names PREMISE.md as the one other root document, which goes when the design is signed.
4. `tracker.py` printed the environment's header inside any project, because it compared the store with the store of the line the caller stands in. It now compares with the environment's own store. Development_Process.md says tracker.md is a generated view of the store that a project may keep or not, so your choice to keep none stands.

**for_you:** Nothing is needed. If you ever want the view, `python <env-root>/Commands/tracker.py --store docs/fragments` now writes `docs/core/tracker.md` with a header about your own store.

**evidence:** `prove_project_initiation.py` checks all four, and restoring the old comparison turns three of its assertions red.
~~~~
