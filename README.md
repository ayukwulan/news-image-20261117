# News Image — Tuesday 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/ayukwulan/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/ayukwulan/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A newspaper front page summing up the real world news of Tuesday
17 November 2026, drawn entirely with PIL shapes (no photographs).

## The stories

1. **Lead — Kerch Bridge severed.** Ukraine's strikes badly damage the
   road and rail bridge linking Russia to Crimea: the road arch is down,
   270m of roadway destroyed, rail damaged, traffic halted. Russia
   retaliates with ballistic missiles hitting Kyiv's Southern and
   Northern bridges; 306 drones in one overnight attack.
2. **Gaza.** The UK, Australia, Canada and Italy jointly urge Israel to
   open Gaza crossings for humanitarian aid; the situation is described
   as catastrophic.
3. **APEC Shenzhen.** Putin arrives in Shenzhen for the APEC summit; a
   first-ever Trump–Xi–Putin trilateral meeting is set; Xi urges free
   trade.
4. **Japan.** Russian aircraft violate Japanese airspace; Japan scrambles
   fighter jets and protests.
5. **Depardieu.** French actor Gérard Depardieu drops his appeal and
   admits a sexual assault charge in a Paris court.
6. **Yemen.** A Houthi advance forces Yemeni government forces to
   retreat from the Red Sea coast to defend Aden.
7. **Also in the news.** Mongolia: President Ukhnaagiin Khürelsükh
   resigns amid a corruption scandal. US: loses measles elimination
   status after 26 years (5,400+ cases, 10 deaths).

## Sources

BBC · Foreign Exchanges · Standard Topic · Meanwhile in Ukraine
(Patreon).

## Files

- `draw.py` — PIL script that draws `entry.png` (1024×1024).
- `entry.png` — the finished front page.
- `main.py` — stdlib-only entry program: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

## Design notes

Masthead "THE WORLD TODAY" with the date in a black band so it reads
at small size. The lead story takes the top half: a large serif
headline, a drawn Kerch Bridge (deck broken at the gap, arch snapped
and drooping, smoke, 270m label), and a fact column plus the Russian
retaliation. Five more stories sit in a 3×2 grid, each with a short
headline, a one-line summary and a small drawn icon (aid box, globe,
jet, gavel, map pin); the sixth cell holds the two optional items.
Light paper background, dark text, no invented facts, no hype.

## Verification

- `entry.png` is exactly 1024×1024 and 122,471 bytes (under the 1 MiB
  cap).
- `main.py` run twice to two different output dirs produces
  byte-identical files (matching sha256).
- The image was viewed and checked: date legible, all headlines
  readable, no overlapping or cut-off text.

## How to run

```sh
python3 draw.py          # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` uses only the Python standard library and runs offline; two
runs write byte-identical files.
