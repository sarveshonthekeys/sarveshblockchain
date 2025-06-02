import random
def generate_shares(secret, k, n, prime):
    
    if k > n:
        raise ValueError("Threshold k cannot be greater than number of shares n.")
    
    
    coeffs = [secret] + [random.randint(0, prime - 1) for _ in range(k - 1)]

    shares = []
    for i in range(1, n + 1):
        x = i
        y = sum([coeff * (x ** idx) for idx, coeff in enumerate(coeffs)]) % prime
        shares.append((x, y))
    
    return shares


def reconstruct_secret(shares, prime):
   
    def lagrange(j, x_values):
       
        xj, _ = x_values[j]
        numerator, denominator = 1, 1
        for m, (xm, _) in enumerate(x_values):
            if m != j:
                numerator = (numerator * -xm) % prime
                denominator = (denominator * (xj - xm)) % prime
        return numerator * pow(denominator, -1, prime) % prime

    secret = 0
    for j, (xj, yj) in enumerate(shares):
        lj = lagrange(j, shares)
        secret = (secret + (yj * lj)) % prime
    return secret

if __name__ == "__main__":
    
    secret = 1234         
    n = 5                   
    k = 3                   
    prime = 2089            
    print(f"\nOriginal Secret: {secret}")

    
    shares = generate_shares(secret, k, n, prime)
    print("\nGenerated Shares:")
    for share in shares:
        print(share)

    
    selected_shares = random.sample(shares, k)
    print("\nSelected Shares for Reconstruction:")
    for share in selected_shares:
        print(share)

    
    recovered_secret = reconstruct_secret(selected_shares, prime)
    print(f"\nReconstructed Secret: {recovered_secret}")
