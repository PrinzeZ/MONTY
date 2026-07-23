"""Not a full test suite — a scripted run through MONTY's CLI covering every
command category, checking the expected output actually appears."""
import io
from contextlib import redirect_stdout

import monty


def run_script(lines):
    inputs = iter(lines)
    buf = io.StringIO()
    with redirect_stdout(buf):
        monty.run(input_func=lambda prompt="": next(inputs))
    return buf.getvalue()


script = [
    "Prinze",                       # name prompt on first run
    "ADD 2 3",
    "SUB 10 4",
    "MULTIPLY 6 7",
    "DIVIDE 10 4",
    "MOD 10 3",
    "POWER 2 10",
    "SQRT 81",
    "LCM 4 6",
    "HCF 12 18",
    "NCR 5 2",
    "NPR 5 2",
    "FACTORIAL 6",
    "ISPRIME 97",
    "FACTORS 360",
    "PERFECT 28",
    "ARMSTRONG 153",
    "PALINDROME 12321",
    "SIMPLIFY sin(x)**2 + cos(x)**2",
    "DIFFERENTIATE x**3 + 2*x",
    "INTEGRATE x**2",
    "INTEGRATE x FROM 0 TO 2",
    "LIMIT sin(x)/x AT 0",
    "SOLVE x**2 - 5*x + 6",
    "SOLVE 2*x + 3 = 7",
    "DETERMINANT [[1,2],[3,4]]",
    "INVERSE [[1,2],[3,4]]",
    "TRANSPOSE [[1,2],[3,4]]",
    "MATRIXMULTIPLY [[1,2]] * [[1],[2]]",
    "STATS 1 2 3 4 5",
    "CONVERT 5 miles to km",
    "CONVERT 100 C to F",
    "NOTE buy milk",
    "NOTES",
    "TIME",
    "DATE",
    "JOKE",
    "asdkjaksjd nonsense",   # unknown command -> confused face, no crash
    "DIVIDE 5 0",            # zero division -> error face, no crash
    "EXIT",
]

output = run_script(script)
print(output)  # so a human reviewing test output can eyeball it

checks = [
    "Nice to meet you, Prinze",
    "2 + 3 = 5", "10 - 4 = 6", "6 * 7 = 42", "10 / 4 = 2.5",
    "10 mod 3 = 1", "2 ^ 10 = 1024", "sqrt(81) = 9.0",
    "LCM(4, 6) = 12", "HCF/GCD(12, 18) = 6",
    "5C2 = 10", "5P2 = 20", "6! = 720",
    "97 is a prime", "Prime factors of 360",
    "28 is a perfect", "153 is an Armstrong", "12321 is a palindrome",
    "Simplified: 1", "d/dx = 3*x**2 + 2",
    "Integral = x**3/3 + C", "Integral = 2",
    "Limit = 1", "Solutions: [2, 3]", "Solutions: [2]",
    "Determinant = -2", "Inverse =", "Transpose =", "Product =",
    "Stats —", "8.04672", "212.0",
    "Noted!", "buy milk", "currently", "Today is",
    "beyond my ability",  # unknown command handled gracefully
    "Can't divide by zero",  # zero division handled gracefully
    "Solved", "Thanks for enjoying it with me",
]

missing = [c for c in checks if c not in output]
assert not missing, f"Missing expected output: {missing}"
print("\nAll MONTY CLI checks passed.")
