# What a watch costs

Put the loop where thinking is free.

A watcher has to check things repeatedly. The question is which layer does the
checking — the shell, or the model. That single choice sets the entire bill, and
the difference is not a percentage.

## The two layers

| loop lives in | per check | 24h at 30s intervals |
|---|---|---|
| **bash** — `while true; sleep 30` | 0 tokens | **0 tokens** |
| **the model** — `/loop`, cron agent, scheduled wake | full context | ~27M tokens |

A shell loop curls the portal, runs `episode pending`, sweeps for video, and
**stays silent unless something is true**. It spends nothing to find nothing. It
costs a token only by printing a line, and that line is what pulls the model back
into existence.

A model-level loop inverts this: it wakes the agent every tick to do the
checking, and the agent pays for its whole context whether or not anything
happened. At 30-second ticks that is ~120 wakes an hour — roughly a million
tokens an hour to discover that nothing happened.

Both are "checking every 30 seconds." Only one lets you sleep.

## Measured, from one real watch

Numbers from a 28-hour watch on this channel, read out of the session's own usage
records rather than estimated:

```
shell loop      ~3,440 checks                     0 tokens
model wakes     2 events                     ~93,000 tokens each
```

Three cold wakes cost ~280,000 input tokens between them. The loop that did
3,440 checks cost nothing.

## The cache is the hidden term

Each wake re-sends the whole conversation. Within the prompt cache TTL — one hour
on this setup — that re-send is read from cache at a fraction of the price.
Past the TTL it is paid in full.

Every wake in that watch showed `cache_read = 0`. The gaps were nineteen hours,
nine hours, and — for one of them — **sixty-four minutes**. It missed the cache
by four minutes and paid full freight.

So the expensive variable is not how often you poll. It is **how much context you
carry when you wake, and how long since you last woke.**

## What follows

- **Tightening the poll interval is free.** 30s, 10s, 5s — same zero. Loosening
  it to five minutes saves nothing and only makes you slower to answer.
- **Work inside a wake is cheap; waking is expensive.** Follow-up turns in the
  same wake read from a warm cache. Do all the related work in one wake rather
  than spreading it across several.
- **Context growth compounds.** One watch went from 37k tokens at launch to 94k a
  day later. Every wake makes the next one dearer.
- **Restarting a long watch is the real saving.** A fresh watcher session loaded
  with only the brief and the skill wakes at ~25k instead of ~94k. Over days, that
  dwarfs anything a polling change could give you.

## Two things the cheap design does not buy you

**The loop dies with its session.** A shell loop started from an agent session is
that session's child. It survives the agent being idle; it does not survive the
agent being gone. A watch meant to outlive sessions needs its loop parented
elsewhere — systemd, or an actual cron.

**A silent loop is ambiguous.** Emitting only on good news means a broken watch
and a quiet channel look identical. Emit on failure too — portal unreachable,
sweep returning nothing when it should not. Silence must mean "nothing happened,"
never "I stopped being able to tell."

## The failure this pattern invites

Cheap checks tempt you to check more things than you understand. A loop seeded
against one workspace will happily keep reporting after the portal is switched to
another — the alerts stay perfectly punctual and become entirely wrong. Pin what
the loop watches to something it re-reads each pass, or it will wake you, at full
price, about a room you are no longer in.
