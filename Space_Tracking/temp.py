total = 0

for a in range(100):
    for b in range(100):
        for c in range(100):
            for d in range(100):
                for e in range(100):
                    if a ** 5 + b ** 5 + c ** 5 + d ** 5 == e ** 5:
                        total = a + b + c + d + e

print(total)
