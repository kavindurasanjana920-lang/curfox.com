# Curfox landing page — going live

## 1. Verify the Calendly embed on your real domain

The lead form has been replaced by Calendly's inline scheduler. There is no
backend and nothing to configure — `CALENDLY_URL` and the widget's `data-url`
both point at `namal_att/courier_growth_strategy_session`.

**This needs one check before launch.** The embed could not be confirmed
rendering from a local `http://localhost` server — the iframe loads but paints
blank, which is typical for third-party embeds that expect a real HTTPS origin.
Deploy to a staging URL over HTTPS and confirm the scheduler actually appears.

If it does not render there either, the usual causes are:

- The site is not served over HTTPS.
- The domain is blocked under Calendly's embed settings for the event type.
- An ad blocker or strict tracking protection is blocking `assets.calendly.com`.

### The page fails safe

Readiness is judged on Calendly's own `postMessage`, not on whether an iframe
element exists — a blocked embed still creates an iframe, and an empty white box
gives a visitor no way to book. If no Calendly message arrives within 8 seconds,
the widget is replaced by a card with an **Open the booking page** button
pointing at the same Calendly URL. A `<noscript>` version covers JavaScript
being off entirely. This fallback is verified working.

### Lead qualification

The old form asked for **deliveries per month**, which qualified the lead before
the call. A bare Calendly booking loses that. Add it back as a required custom
question on the event type in Calendly so it still reaches you with the booking.

### Colours

Calendly's `background_color` / `text_color` / `primary_color` URL parameters
are a paid-plan feature and were ignored, so they have been removed. The widget
renders white and is framed as a white card against the navy band deliberately.
If you upgrade, add those params back to the `data-url`.

## 2. Contact details

Both numbers appear twice — beside the scheduler ("Rather talk right now?") and
in the footer under "Talk to us":

- `+94 77 943 6364` → `tel:+94779436364`
- `+94 11 422 6900` → `tel:+94114226900`

## 3. Social links

In the footer under "Follow Curfox":

- Facebook — <https://www.facebook.com/curfoxdms>
- YouTube — <https://www.youtube.com/@curfox>
- LinkedIn — <https://www.linkedin.com/showcase/curfox>

## 4. Still to do

- Testimonial videos 3 and 4 are labelled "Client testimonial" — their YouTube
  titles don't name the company. Send the names and they can be added.
- The first testimonial headline says 12 parcels (from the video title); the
  thumbnail art says 10. Worth reconciling.

## 5. Rebuilding the shareable preview

`index.html` + `styles.css` + `assets/` is the deployable site. To regenerate the
single-file version for sharing:

```
python3 build-artifact.py
```

It inlines the CSS and every asset as data URIs into `dist/curfox-landing.html`.

Two things only work on your own domain, not in the shared preview, because the
preview host blocks external scripts and frames: **click-to-play video** and the
**Calendly embed**. Both have working fallbacks there — "Watch on YouTube" links
and the "Open the booking page" button.
