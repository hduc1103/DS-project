import random
from sympy import isprime, mod_inverse, gcd

def generate_large_prime():
    while True:
        p = random.randint(1000, 9999)
        if isprime(p):
            return p

def find_primitive_root(p):
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in range(2, p)):
            return g

def generate_keys():
    p = generate_large_prime()
    g = find_primitive_root(p)
    x = random.randint(1, p - 2)  # private key
    y = pow(g, x, p)  # public key
    return (p, g, y), x

def sign_message(private_key, message, p, g):
    x = private_key
    while True:
        k = random.randint(1, p - 2)
        if gcd(k, p - 1) == 1:
            break
    r = pow(g, k, p)
    k_inv = mod_inverse(k, p - 1)
    s = (k_inv * (message - x * r)) % (p - 1)
    return r, s

def verify_signature(public_key, message, signature):
    p, g, y = public_key
    r, s = signature
    if r <= 0 or r >= p:
        return False
    v1 = pow(g, message, p)
    v2 = (pow(y, r, p) * pow(r, s, p)) % p
    return v1 == v2

def main():
    print("=== ElGamal Digital Signature ===")

    # Key generation
    print("Generating keys...")
    public_key, private_key = generate_keys()
    p, g, y = public_key
    print(f"Public Key: p={p}, g={g}, y={y}")
    print(f"Private Key: x={private_key}")

    # Message input
    message = int(input("Enter a message to sign (as a number): "))

    # Signing the message
    print("Signing the message...")
    signature = sign_message(private_key, message, p, g)
    print(f"Signature: r={signature[0]}, s={signature[1]}")

    # Verifying the signature
    print("Verifying the signature...")
    is_valid = verify_signature(public_key, message, signature)
    if is_valid:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")

if __name__ == "__main__":
    main()
