# Freelief: the owner's request

Stated by the owner in chat on 2026-10-07. The words in the quotation are his. The notes below
the quotation are the session's reading of them and are not decided.

> I need a panic attack / anxiety relief web app through GitHub - accessible like Effigy Arcade is.
> Let's just call it freelief.

## The reading of "accessible like Effigy Arcade is"

Two meanings are possible, and the design interview must ask which one he means, or both.

1. **Reachable.** Effigy Arcade is a progressive web app. It is served from GitHub Pages, so a push
   to `main` deploys it. It has no framework, no dependency, no build step and no network call at
   launch. It is phone first and installs to the home screen. This reading says Freelief ships the
   same way.
2. **Usable by anyone, in distress.** A person in a panic attack has little attention, shaky hands
   and sometimes a screen reader or reduced motion switched on. This reading says Freelief meets
   an accessibility standard as a design rule, and not as a late check.

## Facts the interview should start from

- The name is Freelief. The repository name is expected to be `freelief`, under the EffigyMedia
  account, as Effigy Arcade is `effigy-arcade`. Nothing is created on GitHub until the owner says so.
- The product is used in a moment of crisis. It must work with no network, load at once, and ask
  nothing of the person before it helps.
- It is a self-help tool and not medical care. The interview must decide what the product says
  about that, and what it shows a person who may be in danger (a crisis line by region).
- It must not collect or send personal data. A person's worst moments are not telemetry.

## Not yet decided

Who it is for, which techniques it offers (for example paced breathing, grounding, a way to
log an episode), whether it speaks aloud, which languages, and whether it joins a set.
