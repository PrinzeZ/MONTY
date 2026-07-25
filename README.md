# MONTY — Terminal Math & Personal Assistant

A command-line assistant that started as a small four-function calculator
and grew into a proper math engine (symbolic algebra and calculus, matrices,
statistics, number theory) with a bit of personality — it remembers your
name, keeps notes, tells the time, and has an ASCII "face" that reacts to
what just happened.

```
(^_^)/  Good evening, Prinze! MONTY here — HELP if you need a refresher.

> DIFFERENTIATE x**3 + 2*x
(^o^)/  d/dx = 3*x**2 + 2

> SOLVE x**2 - 5*x + 6
(^o^)/  Solutions: [2, 3]

> asdkjaksjd
(-_-;)  Sorry, that's beyond my ability right now — HELP for what I can do.
```

## Setup

```bash
pip install -r requirements.txt
python monty.py
```

## What it can do

| Category | Examples |
|---|---|
| Arithmetic | `ADD 2 3`, `DIVIDE 10 4`, `POWER 2 10`, `SQRT 81` |
| Number theory | `LCM 4 6`, `FACTORIAL 6`, `ISPRIME 97`, `FACTORS 360`, `PERFECT 28`, `ARMSTRONG 153`, `PALINDROME 12321` |
| Combinatorics | `NCR 5 2`, `NPR 5 2` |
| Algebra & calculus | `SIMPLIFY`, `EXPAND`, `FACTOR <expr>` · `DIFFERENTIATE <expr>` · `INTEGRATE <expr> [FROM a TO b]` · `LIMIT <expr> AT <point>` · `SOLVE <expr or lhs = rhs>` |
| Matrices | `DETERMINANT`/`INVERSE`/`TRANSPOSE [[1,2],[3,4]]`, `MATRIXMULTIPLY [[1,2]] * [[1],[2]]` |
| Statistics | `STATS 1 2 3 4 5` — count, mean, median, mode(s), variance, stdev |
| Conversions | `CONVERT 5 miles to km` (length, weight, or C/F/K temperature) |
| Assistant | `NAME <yours>`, `NOTE <text>`, `NOTES`, `CLEARNOTES`, `TIME`, `DATE`, `JOKE` |
| Session | `HELP`, `EXIT` / `QUIT` / `BYE` / `CLOSE` |

The algebra/calculus/matrix commands are backed by [SymPy](https://www.sympy.org/),
a real symbolic math library — that's genuinely solving equations and taking
derivatives, not pattern-matching canned answers.

MONTY remembers your name and notes between runs (in `monty_profile.json` /
`monty_notes.json`, both gitignored so your own data never gets committed).

## Project structure

```
monty_core.py     # All math + assistant logic — no input()/print(), fully testable
monty.py          # Terminal front end: parsing, personality, ASCII faces
test_monty.py     # Scripted run through every command category
requirements.txt
```

## Testing

```bash
python test_monty.py
```

Scripts a full session — every command category, plus an unrecognized
command and a divide-by-zero — and checks MONTY handles all of it without
crashing.

## Notes on the original code

The original `newproject.py` had a few real bugs beyond rough edges: the
perfect-number/Armstrong-number/palindrome checks were written as loose code
at the bottom of the file referencing variables (`r`, `sum`, `total`) that
were never defined at that scope, so the file would crash with a
`NameError` the moment it ran — they never actually worked. They're now
proper, tested functions (`is_perfect`, `is_armstrong`, `is_palindrome` in
`monty_core.py`), and the Armstrong check is generalized to any number of
digits instead of assuming exactly 3.
