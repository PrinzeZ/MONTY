"""
MONTY — your terminal math & personal assistant.

Run with: python monty.py
Type HELP once it's running for the full command list.
"""

import re
import sys
from ast import literal_eval
from datetime import datetime

import monty_core as core

FACES = {
    "idle": "(^_^)",
    "happy": "(^o^)/",
    "thinking": "(o_O)?",
    "confused": "(-_-;)",
    "error": "(x_x)",
    "cool": "(⌐■_■)",
    "wave": "(^_^)/",
    "shrug": r"¯\(-_-)/¯",
}


def say(message, face="happy"):
    print(f"{FACES.get(face, '')}  {message}")


# ---------------------------------------------------------------------
# Small parsing helpers
# ---------------------------------------------------------------------
NUMBER_RE = re.compile(r"-?\d+\.?\d*")


def extract_numbers(text):
    return [float(n) for n in NUMBER_RE.findall(text)]


def as_int_if_whole(value):
    return int(value) if float(value).is_integer() else value


def parse_matrix(text):
    """Turns '[[1,2],[3,4]]' into [[1,2],[3,4]] safely (no eval())."""
    try:
        matrix = literal_eval(text.strip())
    except (ValueError, SyntaxError) as e:
        raise ValueError("Give me a matrix like [[1,2],[3,4]].") from e
    if not (isinstance(matrix, list) and matrix and all(isinstance(r, list) for r in matrix)):
        raise ValueError("Give me a matrix like [[1,2],[3,4]].")
    return matrix


# ---------------------------------------------------------------------
# Command handlers — each takes the text AFTER the command word and
# returns either a message string, or (message, face_key).
# ---------------------------------------------------------------------
def _two_numbers(args):
    nums = extract_numbers(args)
    if len(nums) < 2:
        raise ValueError("I need two numbers for that.")
    return nums[0], nums[1]


def _one_number(args):
    nums = extract_numbers(args)
    if not nums:
        raise ValueError("I need a number for that.")
    return nums[0]


def h_add(args):
    a, b = _two_numbers(args)
    return f"{as_int_if_whole(a)} + {as_int_if_whole(b)} = {as_int_if_whole(core.add(a, b))}"


def h_sub(args):
    a, b = _two_numbers(args)
    return f"{as_int_if_whole(a)} - {as_int_if_whole(b)} = {as_int_if_whole(core.sub(a, b))}"


def h_mul(args):
    a, b = _two_numbers(args)
    return f"{as_int_if_whole(a)} * {as_int_if_whole(b)} = {as_int_if_whole(core.mul(a, b))}"


def h_div(args):
    a, b = _two_numbers(args)
    return f"{as_int_if_whole(a)} / {as_int_if_whole(b)} = {core.div(a, b)}"


def h_mod(args):
    a, b = _two_numbers(args)
    return f"{as_int_if_whole(a)} mod {as_int_if_whole(b)} = {as_int_if_whole(core.mod(a, b))}"


def h_power(args):
    a, b = _two_numbers(args)
    return f"{as_int_if_whole(a)} ^ {as_int_if_whole(b)} = {as_int_if_whole(core.power(a, b))}"


def h_sqrt(args):
    a = _one_number(args)
    return f"sqrt({as_int_if_whole(a)}) = {core.square_root(a)}"


def h_lcm(args):
    a, b = _two_numbers(args)
    return f"LCM({int(a)}, {int(b)}) = {core.lcm(a, b)}"


def h_hcf(args):
    a, b = _two_numbers(args)
    return f"HCF/GCD({int(a)}, {int(b)}) = {core.hcf(a, b)}"


def h_ncr(args):
    n, r = _two_numbers(args)
    return f"{int(n)}C{int(r)} = {core.n_choose_r(n, r)}"


def h_npr(args):
    n, r = _two_numbers(args)
    return f"{int(n)}P{int(r)} = {core.n_permute_r(n, r)}"


def h_factorial(args):
    n = _one_number(args)
    return f"{int(n)}! = {core.factorial(n)}"


def h_isprime(args):
    n = _one_number(args)
    return f"{int(n)} is {'a prime' if core.is_prime(n) else 'not a prime'} number."


def h_factors(args):
    n = _one_number(args)
    return f"Prime factors of {int(n)}: {core.prime_factors(n)}"


def h_perfect(args):
    n = _one_number(args)
    return f"{int(n)} is {'a perfect' if core.is_perfect(n) else 'not a perfect'} number."


def h_armstrong(args):
    n = _one_number(args)
    return f"{int(n)} is {'an Armstrong' if core.is_armstrong(n) else 'not an Armstrong'} number."


def h_palindrome(args):
    n = _one_number(args)
    return f"{int(n)} is {'a palindrome' if core.is_palindrome(n) else 'not a palindrome'}."


def h_simplify(args):
    return f"Simplified: {core.simplify_expr(args)}"


def h_expand(args):
    return f"Expanded: {core.expand_expr(args)}"


def h_factor(args):
    return f"Factored: {core.factor_expr(args)}"


def h_differentiate(args):
    return f"d/dx = {core.differentiate(args)}"


def h_integrate(args):
    match = re.match(r"(.+?)\s+FROM\s+(.+?)\s+TO\s+(.+)", args, re.IGNORECASE)
    if match:
        expr, lower, upper = match.groups()
        return f"Integral = {core.integrate_expr(expr, lower=lower, upper=upper)}"
    return f"Integral = {core.integrate_expr(args)} + C"


def h_limit(args):
    match = re.match(r"(.+?)\s+AT\s+(.+)", args, re.IGNORECASE)
    if not match:
        raise ValueError("Try: LIMIT <expression> AT <point>  (e.g. LIMIT sin(x)/x AT 0)")
    expr, point = match.groups()
    return f"Limit = {core.evaluate_limit(expr, point)}"


def h_solve(args):
    solutions = core.solve_equation(args)
    return f"Solutions: {solutions}"


def h_determinant(args):
    return f"Determinant = {core.matrix_determinant(parse_matrix(args))}"


def h_inverse(args):
    return f"Inverse =\n{core.matrix_inverse(parse_matrix(args))}"


def h_transpose(args):
    return f"Transpose =\n{core.matrix_transpose(parse_matrix(args))}"


def h_matrixmultiply(args):
    if "*" not in args:
        raise ValueError("Try: MATRIXMULTIPLY [[1,2]] * [[1],[2]]")
    left, right = args.split("*", 1)
    return f"Product =\n{core.matrix_multiply(parse_matrix(left), parse_matrix(right))}"


def h_stats(args):
    numbers = extract_numbers(args)
    summary = core.stats_summary(numbers)
    lines = [f"{key}: {value}" for key, value in summary.items()]
    return "Stats —\n  " + "\n  ".join(lines)


def h_convert(args):
    match = re.match(r"(-?\d+\.?\d*)\s*([a-zA-Z]+)\s+(?:to|in)\s+([a-zA-Z]+)", args, re.IGNORECASE)
    if not match:
        raise ValueError("Try: CONVERT 5 miles to km  (length, weight, or C/F/K temperature)")
    value, from_unit, to_unit = match.groups()
    value = float(value)
    for converter in (core.convert_length, core.convert_weight, core.convert_temperature):
        try:
            result = converter(value, from_unit, to_unit)
            return f"{value} {from_unit} = {round(result, 6)} {to_unit}"
        except ValueError:
            continue
    raise ValueError(f"I don't recognize the units '{from_unit}'/'{to_unit}'.")


# ---------------------------------------------------------------------
# Assistant commands
# ---------------------------------------------------------------------
def make_assistant_handlers(state):
    def h_name(args):
        name = args.strip() or None
        if not name:
            raise ValueError("Tell me your name too — e.g. NAME Alex")
        state["profile"]["name"] = name
        core.save_profile(state["profile"])
        return f"Nice to meet you, {name}! I'll remember that.", "wave"

    def h_note(args):
        if not args.strip():
            raise ValueError("What should the note say? e.g. NOTE buy milk")
        core.save_note(args.strip())
        return "Noted!", "cool"

    def h_notes(args):
        notes = core.load_notes()
        if not notes:
            return "You don't have any notes yet."
        lines = [f"{i+1}. {n['text']}  ({n['created']})" for i, n in enumerate(notes)]
        return "Your notes —\n  " + "\n  ".join(lines)

    def h_clearnotes(args):
        core.clear_notes()
        return "All notes cleared."

    def h_time(args):
        return f"It's currently {datetime.now().strftime('%H:%M:%S')}."

    def h_date(args):
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    def h_joke(args):
        import random
        return random.choice(core.JOKES), "cool"

    return {
        "NAME": h_name, "NOTE": h_note, "NOTES": h_notes, "CLEARNOTES": h_clearnotes,
        "TIME": h_time, "DATE": h_date, "JOKE": h_joke,
    }


MATH_HANDLERS = {
    "ADD": h_add, "PLUS": h_add, "SUM": h_add,
    "SUB": h_sub, "SUBTRACT": h_sub, "MINUS": h_sub, "DIFFERENCE": h_sub,
    "MUL": h_mul, "MULTIPLY": h_mul, "PRODUCT": h_mul, "TIMES": h_mul,
    "DIV": h_div, "DIVIDE": h_div, "DIVISION": h_div,
    "MOD": h_mod, "REMAINDER": h_mod, "MODULUS": h_mod,
    "POWER": h_power, "EXPONENT": h_power,
    "SQRT": h_sqrt, "ROOT": h_sqrt,
    "LCM": h_lcm, "HCF": h_hcf, "GCD": h_hcf,
    "NCR": h_ncr, "COMBINATION": h_ncr,
    "NPR": h_npr, "PERMUTATION": h_npr,
    "FACTORIAL": h_factorial,
    "ISPRIME": h_isprime, "PRIME": h_isprime,
    "FACTORS": h_factors, "PRIMEFACTORS": h_factors,
    "PERFECT": h_perfect, "ISPERFECT": h_perfect,
    "ARMSTRONG": h_armstrong, "ISARMSTRONG": h_armstrong,
    "PALINDROME": h_palindrome, "ISPALINDROME": h_palindrome,
    "SIMPLIFY": h_simplify,
    "EXPAND": h_expand,
    "FACTOR": h_factor,
    "DIFFERENTIATE": h_differentiate, "DERIVATIVE": h_differentiate, "DIFF": h_differentiate,
    "INTEGRATE": h_integrate, "INTEGRAL": h_integrate,
    "LIMIT": h_limit,
    "SOLVE": h_solve,
    "DETERMINANT": h_determinant, "DET": h_determinant,
    "INVERSE": h_inverse,
    "TRANSPOSE": h_transpose,
    "MATRIXMULTIPLY": h_matrixmultiply,
    "STATS": h_stats, "STATISTICS": h_stats,
    "CONVERT": h_convert,
}

HELP_TEXT = """\
Arithmetic       ADD/SUB/MULTIPLY/DIVIDE/MOD/POWER a b, SQRT a
Number theory    LCM a b, HCF a b, FACTORIAL a, ISPRIME a, FACTORS a,
                 PERFECT a, ARMSTRONG a, PALINDROME a
Combinatorics    NCR n r, NPR n r
Algebra/calculus SIMPLIFY, EXPAND, FACTOR <expr>
                 DIFFERENTIATE <expr>
                 INTEGRATE <expr> [FROM a TO b]
                 LIMIT <expr> AT <point>
                 SOLVE <expr or lhs = rhs>
Matrices         DETERMINANT/INVERSE/TRANSPOSE [[1,2],[3,4]]
                 MATRIXMULTIPLY [[1,2]] * [[1],[2]]
Statistics       STATS 1 2 3 4 5
Conversions      CONVERT 5 miles to km   (length, weight, or C/F/K temperature)
Assistant        NAME <yours>, NOTE <text>, NOTES, CLEARNOTES, TIME, DATE, JOKE
Session          HELP, EXIT / QUIT / BYE / CLOSE
"""


def h_help(args):
    return HELP_TEXT


# ---------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------
def run(input_func=input):
    state = {"profile": core.load_profile(), "solved_count": 0}
    handlers = {**MATH_HANDLERS, **make_assistant_handlers(state), "HELP": h_help}
    exit_words = {"EXIT", "QUIT", "CLOSE", "BYE"}

    name = state["profile"].get("name")
    if name:
        say(f"{core.greeting_for_now()}, {name}! MONTY here — HELP if you need a refresher.", "wave")
    else:
        say(f"{core.greeting_for_now()}! I'm MONTY. What should I call you?", "wave")
        entered = input_func("> ").strip()
        if entered:
            state["profile"]["name"] = entered
            core.save_profile(state["profile"])
            say(f"Nice to meet you, {entered}! Type HELP any time to see what I can do.", "happy")

    while True:
        try:
            text = input_func("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            say("Bye for now!", "wave")
            break

        if not text:
            continue

        command, _, args = text.partition(" ")
        command = command.upper()

        if command in exit_words:
            say(f"Solved {state['solved_count']} things this session. Thanks for enjoying it with me!", "wave")
            break

        handler = handlers.get(command)
        if not handler:
            say("Sorry, that's beyond my ability right now — HELP for what I can do.", "confused")
            continue

        try:
            result = handler(args)
            message, face = result if isinstance(result, tuple) else (result, "happy")
            say(message, face)
            state["solved_count"] += 1
        except ZeroDivisionError as e:
            say(str(e), "error")
        except (ValueError, TypeError) as e:
            say(str(e), "confused")
        except Exception as e:  # sympy/parsing surprises shouldn't crash the session
            say(f"Something went wrong with that: {e}", "error")


if __name__ == "__main__":
    run()
