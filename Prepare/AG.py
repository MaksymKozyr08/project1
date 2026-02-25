def horner_scheme(coefficients, alpha):
    n = len(coefficients)
    # Створюємо список для коефіцієнтів частки та остачі
    # Перший коефіцієнт завжди переноситься без змін
    results = [coefficients[0]]
    
    # Обчислюємо за формулою: b_k = a_k + alpha * b_{k-1}
    for i in range(1, n):
        next_val = coefficients[i] + alpha * results[i-1]
        results.append(next_val)
    
    # Виведення таблиці
    print(f"\nСхема Горнера для ділення на (x - ({alpha}))")
    print("-" * (n * 10 + 15))
    
    
    # Рядок вихідних коефіцієнтів
    header = " Коеф. a_i | " + " | ".join(f"{c:^7}" for c in coefficients)
    print(header)
    print("-" * (n * 10 + 15))
    
    # Рядок результатів b_i
    res_line = f" b_i (a={alpha:^3})| " + " | ".join(f"{r:^7}" for r in results)
    print(res_line)
    print("-" * (n * 10 + 15))
    
    # Аналіз результату
    quotient = results[:-1]
    remainder = results[-1]
    return quotient, remainder

# Дані з твоєї задачі 2.12:
# f(x) = 3x^5 - 2x^4 + 0x^3 + 0x^2 + 5x - 6x + 2 (уточнив за скріном)
# Коефіцієнти: 3, -2, 0, 0, 5, -6, 2 (якщо степінь 5)
# Для x + 1 => alpha = -1

coeffs = [3, -2, 0, 5, -6, 2]  # приклад для f(x) = 3x^5 - 2x^4 + 0x^3 + 5x^2 - 6x + 2
a = -1

q, r = horner_scheme(coeffs, a)

print(f"\nРезультат:")
print(f"Частка q(x) має коефіцієнти: {q}")
print(f"Остача r = {r}")