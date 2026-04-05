R = 13.0 / 6.0

Omega_b = 1 / (3 * R**2 + 3 * R)
Omega_m = 3 * R * Omega_b
Omega_L = 3 * R**2 * Omega_b
Omega_dm = Omega_m - Omega_b

print(Omega_L, Omega_m, Omega_dm, Omega_b)
