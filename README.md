# THE WORLD TODAY — Thursday 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/laithzz21/news-image-20261126-r2/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/laithzz21/news-image-20261126-r2/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for the make.fun bounty
[news-image-20261126](https://make.fun/bounty/news-image-20261126):
sum up the world's news of Thursday 26 November 2026 in one image.

## What it is

`main.py` validates the bundled `entry.png` — a 1024×1024 newspaper
front page, **THE WORLD TODAY** — and copies it byte-identical to the
output path. It uses only the Python standard library: no external
images, no network, no clock, no random numbers, no rendering at run
time. The program checks the PNG magic bytes, the IHDR chunk
(1024×1024, bit depth 8, colour type 2 = RGB), the file size
(at most 1 MiB) and the SHA-256 digest before writing anything.
Running it twice produces byte-identical output.

## The stories on the page

All six stories (plus the footer ticker) are genuine news reported on
Thursday 26 November 2026:

- **Lead — Space:** Muhammad Zeeshan Ali becomes the first foreign
  astronaut to visit China's Tiangong space station, flying aboard
  Shenzhou-24 — a first for Pakistan and a milestone for China's space
  programme.
- **War — Ukraine:** Russia's own figures show nearly 500,000 people
  lost in the Ukraine war; Kyiv says five Russian military jets were
  hit in an airfield strike.
- **Rescue — Colombia:** Police storm a supermarket in Cartagena and
  free 20 people held hostage for 17 hours after a failed cash-truck
  robbery.
- **Trade — Washington:** The US is preparing to unveil a new plan for
  tariffs on global trading partners.
- **Pacific:** Solomon Islands signs a security treaty with Australia,
  seen as a setback for Beijing's influence in the Pacific.
- **Seoul:** South Korea's education minister Choi Kyo-jin resigns
  over an exam-cheating scandal.
- **Also today (footer ticker):** Thanksgiving across America; Mumbai
  marks 18 years since the 26/11 attacks; Venezuela reveals $237bn of
  public debt.

Sources: BBC, NYT, Reuters, AP.

## Run it

```sh
python3 main.py            # validates entry.png and writes it to the output path
python3 main.py --verify   # validate only, no output written
```

Requires only Python 3.13 standard library — no third-party packages.

## License

MIT — see [LICENSE](LICENSE).
