# Freelief

**Help through a panic attack or strong anxiety, right now.** Free, offline and private.

Freelief opens on a short menu with nothing to fill in first. Breathe is first: a guide that helps
you slow your breathing. One tap also reaches gentle activities (pop bubbles, trace a shape, sort
colors, a ripple pond and a mandala to color) and the Visualizer (soft music or rain with slow
shapes). Every screen has a **"Need urgent help?"** button with crisis lines for your country.

- **Free and open source** (MIT license). No account, no advertising, no analytics.
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

## Research and standards

Each technique is built on published research, and the app's **Standards and research** page
lists every source, with an honest note on how strong the evidence is. Freelief is built to meet
WCAG 2.2 level AA, and AAA where it can. It claims a standard only after people have checked it
with a screen reader and a keyboard.

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
