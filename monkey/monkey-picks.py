#!/usr/bin/env python3
"""The Monkey's complete brain — Season 1: "Catch the Index" (2026-08-17 → 2026-11-13).

The Monkey is one of the three contestants in Season 1 (vs Jack, an autonomous
AI paper-trading $100k, and SPY buy-and-hold). It runs $100k with a seeded RNG:
each Monday it picks 5 of the 20 ETFs below at random (uniform, no memory),
equal-weights 95% of the account (5% stays cash, like a real account), and
holds until the next Monday.

The seed is public ON PURPOSE. Every pick is a pure function of
    sha256("<seed>:week<N>")  →  random.Random  →  sample 5 of 20
so anyone can reproduce the Monkey's entire season from this file alone and
check it against the published results. No hidden state, no reruns, no mercy.

This logic is byte-for-byte the pick logic used by the season tracker that
produces the published standings.

Usage:
    python3 monkey-picks.py         # picks for every week of the season (0-12)
    python3 monkey-picks.py 3       # picks for week 3 only

Week 0 begins Monday 2026-08-17; week N covers the trading days starting with
the first trading day on or after (2026-08-17 + 7*N days).
"""
import hashlib
import random
import sys

MONKEY_SEED = "SEASON1-CATCH-THE-INDEX-2026"   # public — reproducibility IS the point
MONKEY_UNIVERSE = ["SPY", "QQQ", "IWM", "EFA", "EEM", "GLD", "SLV", "TLT",
                   "SHY", "XLK", "XLE", "XLF", "XLV", "XLI", "XLU", "XLP",
                   "XLY", "XLB", "SMH", "DBC"]
MONKEY_PICKS = 5
SEASON_WEEKS = 13                               # 2026-08-17 → 2026-11-13


def monkey_picks_for_week(week_index):
    """Deterministic picks: seed + week number → 5 symbols. Reproducible by anyone."""
    seed = hashlib.sha256(f"{MONKEY_SEED}:week{week_index}".encode()).hexdigest()
    rng = random.Random(seed)
    return sorted(rng.sample(MONKEY_UNIVERSE, MONKEY_PICKS))


if __name__ == "__main__":
    weeks = ([int(sys.argv[1])] if len(sys.argv) > 1 else range(SEASON_WEEKS))
    for wk in weeks:
        print(f"week {wk:2d}: {', '.join(monkey_picks_for_week(wk))}")
