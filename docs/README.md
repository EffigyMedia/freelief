# Freelief

**Help through a panic attack or strong anxiety, right now.** Free, offline and private.

Freelief opens on a short menu with nothing to fill in first. Breathe is first: a guide that helps
you slow your breathing. One tap also reaches gentle activities (pop bubbles, trace a shape, the
Unblock puzzle, a ripple pond and a mandala to color) and the Visualizer (slow shapes). Music, rain or waves play from the
buttons at the top, on every screen. Every screen has a **"Need urgent help?"** button with crisis lines for your country.

- **Free and open source** (MIT license). No account, no advertising, no analytics.
  The Effigy Media name and logo are not part of the MIT license; see `LICENSE`.
- **Works offline** once installed to your home screen.
- **Private.** Nothing about you is collected or sent. Your settings stay on your device.
- **Built for everyone.** Touch, keyboard and screen reader all work, reduced motion is honoured,
  and nothing is timed or scored.

> Freelief is a self-help tool. It is not medical care and does not replace a doctor, a therapist
> or emergency services. If you are in danger, call your local emergency number.

## Preview

**Freelief is in preview and not yet released.** A preview build is at
<https://effigymedia.github.io/freelief/> so that people can test it and check it with assistive
technology. Please do not rely on it yet. Version 1.0 will be the first release, after a full
release audit; this page will then say how to install it.

The preview serves **v0.8.8** (moved 2026-10-10 with the owner's yes). Each move of the preview is
recorded in `docs/core/changelog.md` with the owner's yes, and this line names the version it serves.

## Research and accessibility

Slow breathing has good evidence; the activities are gentle distractions, and the evidence for them
is limited. The sources are recorded in `docs/research/sources.md`. Freelief is built to meet WCAG
2.2 level AA, and AAA where it can, and it makes no standards claim in the app.

## Help check it

If you use a screen reader, a keyboard, switch access or other assistive technology, your check
helps more than anything else. Use the **Feedback** page in the app, or open an
[accessibility check](../../../issues/new?template=accessibility-check.md) here.

## For developers

Plain HTML, CSS and JavaScript, with no framework, no dependency and no build step. GitHub Pages
serves the `live` branch of the repository as it is; pushing `main` deploys nothing. Tests use Python and Playwright:

```
python tools/freelief.py setup
python tools/freelief.py test
python tools/freelief.py run
```

The design, the requirements and the decisions are in `docs/`.
