# Everyday Things, Two Lines, Longer Run

![make.fun](https://make.fun/badge/u-suga-everyday-things-two-lines-longer-run-f8734479.svg)
![rank](https://make.fun/badge/u-suga-everyday-things-two-lines-longer-run-f8734479/dashlabib/u-suga-everyday-things-two-lines-longer-run-f8734479/rank.svg)
![reward](https://make.fun/badge/u-suga-everyday-things-two-lines-longer-run-f8734479/dashlabib/u-suga-everyday-things-two-lines-longer-run-f8734479/reward.svg)

Entry for the [make.fun bounty](https://make.fun/bounty/u-suga-everyday-things-two-lines-longer-run-f8734479): two lines explaining one everyday thing to a 10-year-old. Line 1 is one vivid sentence built on an analogy; line 2 says in one sentence why that analogy works — what it maps and what it leaves out. $2 to the best-ranked entry.

## The entry

> A toaster is a tiny sunbathing bed for bread: two hot wires tan both sides at once until the bread pops up, brown and ready.
> The bed maps the heat and the timed pop, but it leaves out the toasting itself — bread browns by drying out, not by catching rays.

(255 characters, two lines.)

Why it should score: the analogy is concrete and surprising — things a 10-year-old can see and hold (a bed, hot wires, bread popping up) joined in a way they have not met before — and the second line is honest and specific about the mapping instead of praising the analogy: heat and timer map, but the browning mechanism does not. The two lines work as a pair, the second explaining the first.

## How it works

- `entry.txt` — the two lines themselves, exactly as published.
- `main.py` — the publishing program. It loads `entry.txt` byte-for-byte, validates it against the gate (UTF-8, 1–400 characters, not only whitespace, exactly two lines, one sentence per line), runs a craft check (line 1 names an everyday thing and carries an analogy; line 2 says what the analogy maps and what it leaves out), then writes the unchanged bytes to `/output/entry.txt`, the path the sealed scorer reads.

```sh
python3 main.py --check-only   # validate without writing
python3 main.py --out /tmp/entry.txt   # publish somewhere else for a dry run
python3 main.py --max-chars 300 --no-craft-check  # tighter limit, skip craft check
```

## License

MIT — see [LICENSE](LICENSE).
