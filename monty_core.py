"""
MONTY — core engine.

All the actual math and assistant logic lives here, with no input()/print().
monty.py (the terminal front end) imports from this module, so every
capability here is independently testable.
"""

import json
import math
import os
import statistics
from datetime import datetime

import sympy
from sympy import symbols, sympify, Eq, solve, diff, integrate, limit, simplify, expand, factor, Matrix
from sympy.parsing.sympy_parser import parse_expr

X = symbols("x")

NOTES_FILE = "monty_notes.json"
PROFILE_FILE = "monty_profile.json"

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, and now it won't stop sending me KitKat ads.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "Why was the equal sign so humble? Because it knew it wasn't less than or greater than anyone else.",
    "There are 10 kinds of people: those who understand binary, and those who don't.",
    "I've got a great joke about infinity, but it never ends.",
    "Why did the student do multiplication problems on the floor? The teacher said not to use tables.",
]


# ---------------------------------------------------------------------
# Basic arithmetic
# ---------------------------------------------------------------------
def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Can't divide by zero.")
    return a / b


def mod(a, b):
    if b == 0:
        raise ZeroDivisionError("Can't take a remainder of division by zero.")
    return a % b


def power(a, b):
    return a**b


def square_root(a):
    if a < 0:
        raise ValueError("Can't take the real square root of a negative number.")
    return math.sqrt(a)


# ---------------------------------------------------------------------
# Number theory (the original file's versions here were broken: dead code
# after `return`, and a block using undefined module-level variables r,
# sum, and total that would crash on import. These are fixed, generalized,
# and made independently callable.)
# ---------------------------------------------------------------------
def lcm(a, b):
    a, b = int(a), int(b)
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def hcf(a, b):
    return math.gcd(int(a), int(b))


def is_prime(n):
    n = int(n)
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_factors(n):
    n = int(n)
    if n < 2:
        return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def is_perfect(n):
    """A perfect number equals the sum of its proper divisors (e.g. 28 = 1+2+4+7+14)."""
    n = int(n)
    if n < 2:
        return False
    total = 1  # 1 always divides n (for n > 1)
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total == n


def is_armstrong(n):
    """Generalized to any number of digits (the original hardcoded **3)."""
    n = int(n)
    digits = str(abs(n))
    power_ = len(digits)
    return sum(int(d) ** power_ for d in digits) == abs(n)


def is_palindrome(n):
    text = str(int(n))
    return text == text[::-1]


def factorial(n):
    n = int(n)
    if n < 0:
        raise ValueError("Factorial isn't defined for negative numbers.")
    return math.factorial(n)


def n_permute_r(n, r):
    return math.perm(int(n), int(r))


def n_choose_r(n, r):
    return math.comb(int(n), int(r))


# ---------------------------------------------------------------------
# Advanced / symbolic math (sympy)
# ---------------------------------------------------------------------
def _parse(expr_str):
    try:
        return parse_expr(expr_str.replace("^", "**"), evaluate=True)
    except Exception as e:
        raise ValueError(f"Couldn't parse '{expr_str}' as a math expression.") from e


def simplify_expr(expr_str):
    return simplify(_parse(expr_str))


def expand_expr(expr_str):
    return expand(_parse(expr_str))


def factor_expr(expr_str):
    return factor(_parse(expr_str))


def differentiate(expr_str, var="x"):
    v = symbols(var)
    return diff(_parse(expr_str), v)


def integrate_expr(expr_str, var="x", lower=None, upper=None):
    v = symbols(var)
    expr = _parse(expr_str)
    if lower is not None and upper is not None:
        return integrate(expr, (v, _parse(str(lower)), _parse(str(upper))))
    return integrate(expr, v)


def evaluate_limit(expr_str, point, var="x"):
    v = symbols(var)
    return limit(_parse(expr_str), v, _parse(str(point)))


def solve_equation(expr_str, var="x"):
    """Accepts either 'expr' (solved for expr = 0) or 'lhs = rhs'."""
    v = symbols(var)
    if "=" in expr_str and "==" not in expr_str:
        lhs, rhs = expr_str.split("=", 1)
        equation = Eq(_parse(lhs), _parse(rhs))
    else:
        equation = Eq(_parse(expr_str), 0)
    return solve(equation, v)


def matrix_determinant(rows):
    return Matrix(rows).det()


def matrix_inverse(rows):
    m = Matrix(rows)
    if m.det() == 0:
        raise ValueError("This matrix is singular (determinant is 0) — it has no inverse.")
    return m.inv()


def matrix_multiply(rows_a, rows_b):
    a, b = Matrix(rows_a), Matrix(rows_b)
    if a.cols != b.rows:
        raise ValueError(f"Can't multiply a {a.rows}x{a.cols} matrix by a {b.rows}x{b.cols} matrix.")
    return a * b


def matrix_transpose(rows):
    return Matrix(rows).T


# ---------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------
def stats_summary(numbers):
    if not numbers:
        raise ValueError("Give me at least one number.")
    summary = {
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "modes": statistics.multimode(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "range": max(numbers) - min(numbers),
    }
    if len(numbers) > 1:
        summary["variance"] = statistics.variance(numbers)
        summary["stdev"] = statistics.stdev(numbers)
    return summary


# ---------------------------------------------------------------------
# Unit conversion
# ---------------------------------------------------------------------
_LENGTH_TO_METERS = {
    "mm": 0.001, "millimeter": 0.001, "millimeters": 0.001, "millimetre": 0.001, "millimetres": 0.001,
    "cm": 0.01, "centimeter": 0.01, "centimeters": 0.01, "centimetre": 0.01, "centimetres": 0.01,
    "m": 1.0, "meter": 1.0, "meters": 1.0, "metre": 1.0, "metres": 1.0,
    "km": 1000.0, "kilometer": 1000.0, "kilometers": 1000.0, "kilometre": 1000.0, "kilometres": 1000.0,
    "in": 0.0254, "inch": 0.0254, "inches": 0.0254,
    "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
    "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
    "mi": 1609.344, "mile": 1609.344, "miles": 1609.344,
}
_WEIGHT_TO_GRAMS = {
    "mg": 0.001, "milligram": 0.001, "milligrams": 0.001,
    "g": 1.0, "gram": 1.0, "grams": 1.0,
    "kg": 1000.0, "kilogram": 1000.0, "kilograms": 1000.0,
    "oz": 28.349523125, "ounce": 28.349523125, "ounces": 28.349523125,
    "lb": 453.59237, "lbs": 453.59237, "pound": 453.59237, "pounds": 453.59237,
}


def convert_length(value, from_unit, to_unit):
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    if from_unit not in _LENGTH_TO_METERS or to_unit not in _LENGTH_TO_METERS:
        raise ValueError(f"I don't know one of these length units: {from_unit}, {to_unit}")
    meters = value * _LENGTH_TO_METERS[from_unit]
    return meters / _LENGTH_TO_METERS[to_unit]


def convert_weight(value, from_unit, to_unit):
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    if from_unit not in _WEIGHT_TO_GRAMS or to_unit not in _WEIGHT_TO_GRAMS:
        raise ValueError(f"I don't know one of these weight units: {from_unit}, {to_unit}")
    grams = value * _WEIGHT_TO_GRAMS[from_unit]
    return grams / _WEIGHT_TO_GRAMS[to_unit]


def convert_temperature(value, from_unit, to_unit):
    from_unit, to_unit = from_unit.upper()[0], to_unit.upper()[0]
    if from_unit not in "CFK" or to_unit not in "CFK":
        raise ValueError("Temperature units must be C, F, or K.")
    # Normalize to Celsius first
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5 / 9
    else:  # K
        celsius = value - 273.15

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius * 9 / 5 + 32
    else:  # K
        return celsius + 273.15


# ---------------------------------------------------------------------
# Personal-assistant utilities
# ---------------------------------------------------------------------
def greeting_for_now():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


def load_notes(path=NOTES_FILE):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_note(text, path=NOTES_FILE):
    notes = load_notes(path)
    notes.append({"text": text, "created": datetime.now().strftime("%Y-%m-%d %H:%M")})
    with open(path, "w") as f:
        json.dump(notes, f, indent=2)
    return notes


def clear_notes(path=NOTES_FILE):
    with open(path, "w") as f:
        json.dump([], f)


def load_profile(path=PROFILE_FILE):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_profile(profile, path=PROFILE_FILE):
    with open(path, "w") as f:
        json.dump(profile, f, indent=2)
