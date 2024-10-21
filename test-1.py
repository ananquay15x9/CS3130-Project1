import time
import random

class LimitedInt:
    MAX_INT = 2**63 - 1
    MIN_INT = -2**63

    def __init__(self, value):
        self.value = value
        self._handle_overflow()

    def _handle_overflow(self):
        if self.value > self.MAX_INT or self.value < self.MIN_INT:
            self.value = self.value % (2**64)
            if self.value > self.MAX_INT:
                self.value -= 2**64

    def __add__(self, other):
        result = LimitedInt(self.value + other.value)
        result._handle_overflow()
        return result

    def __mul__(self, other):
        result = LimitedInt(self.value * other.value)
        result._handle_overflow()
        return result

    def __pow__(self, power):
        result = LimitedInt(self.value ** power)
        result._handle_overflow()
        return result

    def __str__(self):
        return str(self.value)

def brute_force(coeffs, x):
    result = LimitedInt(0)
    for i in range(len(coeffs)):
        result += LimitedInt(coeffs[i]) * (x ** (i + 1))
    return result + LimitedInt(1)

def repeated_squaring(coeffs, x):
    result = LimitedInt(1)  # Start with 1
    x_power = x
    for i in range(len(coeffs)):
        result += LimitedInt(coeffs[i]) * x_power
        x_power = x_power * x 
    return result

def horner(coeffs, x):
    result = LimitedInt(coeffs[-1])
    for i in range(len(coeffs) - 2, -1, -1):
        result = result * x + LimitedInt(coeffs[i])
    return result * x + LimitedInt(1)

def time_function(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    elapsed_time_ms = (end - start) * 1000  # Convert seconds to milliseconds
    return result, elapsed_time_ms

def generate_coefficients(n):
    return list(range(1, n + 1))  # Generates [1, 2, ..., n]

def save_data_to_file(n, d, filename):
    coeffs = generate_coefficients(n)
    x_value = random.randint(0, (10 ** d) - 1)  # Generate x within the range for d digits
    
    with open(filename, 'w') as file:
        file.write(f"{n}\n")
        file.write(f"{d}\n")
        file.write(" ".join(map(str, coeffs)) + "\n")
        file.write(f"{x_value}\n")
    
    print(f"Data saved to {filename}:")

def load_data_from_file(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        d = int(file.readline().strip())
        coeffs = list(map(int, file.readline().strip().split()))
        x_value = int(file.readline().strip())
    
    return n, d, coeffs, LimitedInt(x_value)

def main():
    # Data generation round
    n = int(input("Enter the degree of the polynomial (n): "))
    d = int(input("Enter the number of digits for coefficients and x (d): "))
    
    filename = "polynomial_data.txt"
    save_data_to_file(n, d, filename)

    # Load data and run experiments
    n, d, coeffs, x = load_data_from_file(filename)
    print(f"\nLoaded data from {filename}:\nCoefficients: {coeffs}\nx value: {x}\n==========================================")

    methods = [
        ("Brute Force", brute_force),
        ("Repeated Squaring", repeated_squaring),
        ("Horner's Rule", horner)
    ]
    
    for name, method in methods:
        result, execution_time = time_function(method, coeffs, x)
        print(f"{name}: {result}, Time: {execution_time:.3f} milliseconds\n")

if __name__ == "__main__":
    main()
