"""
Example use case of the Listener functionality:

Bhaskara's theroem deduction
"""

import sympy as sp

# Define symbols
x, a, b, c = sp.symbols("x a b c")

# To solve for the roots of a square function:
# a*x**2 + b*x + c = 0
eq = sp.Equality(a*x**2 + b*x + c, 0)

# Solve the equality for x
solution = sp.solve(eq, x)

# Print the solution
print(solution)

# Get the LaTeX expression
latex = sp.latex(solution)

# Define a name and folder for the expression
expr_name = "Bhaskara's Theorem"
expr_folder = "Basic algebra"

# Now, to send it to the app:
import requests

# Build the payload
payload = {
    "expr":latex,           # MUST HAVE
    "name":expr_name,       # Optional
    "folder":expr_folder    # Optional
}

# "default" is the default socket key
print(requests.post("http://localhost:8501/listener/default", json=payload))

# Done! Now, the expression may show in "See caught expressions" within the app
# You may also send multiple expressions, by using "payload" in the format:
# payload = [
#    {
#    "expr":latex1,
#    "name":expr_name1,
#    "folder":expr_folder1
#    },
#    {
#    "expr":latex2,
#    "name":expr_name2,
#    "folder":expr_folder2
#    }
#]