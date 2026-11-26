# THE WORLD — Thursday 26 November 2026

A one-image newspaper front page summing up the world's news of
Thursday 26 November 2026, built for the make.fun
`news-image-20261126` competition.

## The day's news in the image

- **Lead — Houthis strike Saudi refinery:** Yemen's Houthis claim attacks
  on Ras Tanura, Saudi Arabia's largest refinery, and the Riyadh financial
  district. Brent crude tops $94 on fears for Gulf energy supplies, days
  after the PIF Tower strike in Riyadh wounded 11.
- **Trump readies new tariffs:** the US prepares new tariffs on global
  trading partners — up to 15% on Taiwan goods. Taiwan shares fall
  1,926 points as the NT dollar weakens past 33 per dollar.
- **Cairo tanker fire kills 30:** a fuel tanker crash ignites a huge blaze
  on a highway ringing the Egyptian capital.
- **BepiColombo reaches Mercury:** the ESA/JAXA spacecraft enters Mercury
  orbit after an eight-year journey.
- **North Korea expels Swiss diplomat:** Pyongyang orders Switzerland to
  close its newly opened office in a sanctions row.
- **Gukesh–Sindarov draw:** game 2 of the World Chess Championship ends in
  a 20-move draw.
- **Also today:** Solomon Islands–Australia sign a security treaty; India
  marks the 26/11 anniversary.

## How it is built

`gen_image.py` draws the whole front page with Pillow (pure vector-style
shapes and text — no photos, no network, no clock, no randomness), so the
PNG is byte-identical on every run. `main.ts` (Node 22, standard library
only) copies the generated `entry.png` to the output directory.

```sh
python3 gen_image.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.
