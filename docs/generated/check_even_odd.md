# Documentation for `check_even_odd.py`

Here's the documented version of the Python code:

```python
"""
Module: even_or_odd.py

This module provides a simple program to check if a given number is even or odd.
It prompts the user to input a number and then prints out whether the number is even or odd.
"""

def get_user_input() -> int:
    """
    Prompts the user to input a number and returns the input as an integer.

    Returns:
        int: The number entered by the user.
    """
    return int(input("Enter a number: "))

def is_even(number: int) -> bool:
    """
    Checks if the given number is even.

    Args:
        number (int): The number to be checked.

    Returns:
        bool: True if the number is even, False otherwise.
    """
    return number % 2 == 0

def print_result(number: int) -> None:
    """
    Prints out whether the given number is even or odd.

    Args:
        number (int): The number to be checked.

    Returns:
        None
    """
    if is_even(number):
        print("The number is even.")
    else:
        print("The number is odd.")
    
def main() -> None:
    """
    The main function that runs the program.

    Returns:
        None
    """
    user_input = get_user_input()
    print_result(user_input)

if __name__ == "__main__":
    main()
```

In this code, I've added docstrings to each function, explaining what they do, their parameters, and their return values. I've also added a module-level docstring to provide an overview of the program. Additionally, I've broken down the original code into separate functions for better organization and reusability.