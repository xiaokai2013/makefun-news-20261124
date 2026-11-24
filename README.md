# The World — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/xiaokai2013/makefun-news-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/xiaokai2013/makefun-news-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-image newspaper front page summing up **Tuesday 24 November 2026**,
built for the [make.fun](https://make.fun/bounty/news-image-20261124)
news-image bounty.

## The seven stories

1. **Russian strike kills 2, wounds 22 in Zaporizhzhia** — overnight hit
   wrecks flats; two children among the wounded. (Straits Times / The Hindu)
2. **Russian jets enter Seoul's air defence zone** — Ulleung island sirens
   sound; jets scrambled, alert lifted in minutes. (Yonhap / Reuters)
3. **Iran says three tankers hit mines in Hormuz** — IRGC claims blasts
   under US escort; the reports are unverified. (Al Jazeera / JPost)
4. **UK sanctions Myanmar president after ruling** — London acts days after
   the ICJ found Myanmar guilty of genocide. (SCMP)
5. **Trump targets Newsom in crime speech** — president attacks the
   governor's commutation of 500 death sentences. (SCMP)
6. **Armenia unveils draft constitution** — key to a lasting peace with
   Azerbaijan. (SCMP)
7. **Amtrak derails in Louisiana** — 95 aboard; five hurt after hitting a
   truck. (Times of India)

Every story was checked against reporting published on 24 November 2026.
The Hormuz item is worded as a claim, not a fact, because it was not
independently verified.

## How it works

- `news.json` — the seven verified stories, date line and footer.
- `render.py` — a Pillow renderer that draws the 1024×1024 front page
  (masthead, lead with a drawn skyline strip, 2×2 middle grid, bottom band).
  Run it with `python3 render.py`; run it twice and the md5 is identical.
- `main.py` — the entry point. The grading sandbox has no Pillow and no
  fonts, so this file uses only the standard library: it copies the
  committed `entry.png` to `/output/entry.png`.
- `entry.png` — the finished front page (1024×1024, under 1 MiB).

## Verify

```sh
python3 render.py && md5sum entry.png
python3 render.py && md5sum entry.png   # same md5 both times
```

## License

MIT — see [LICENSE](LICENSE).
