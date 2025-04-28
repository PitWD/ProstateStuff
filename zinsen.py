def calculate_months(initial_capital, monthly_withdrawal, annual_interest_rate):
    # Umrechnung des jährlichen Zinssatzes in monatlichen Zinssatz
    monthly_rate = annual_interest_rate / 12 / 100
    months = 0
    while initial_capital >= monthly_withdrawal:
        # Entnahme
        initial_capital -= monthly_withdrawal
        # Zinsen
        interest = initial_capital * monthly_rate
        if interest > monthly_withdrawal:
            print("\nZinsen sind höher als Entnahme!\nBitte den Zinssatz reduzieren oder die Entnahme erhöhen.")
            break
        # Kapital nach Zinsen
        initial_capital += interest
        months += 1
        if initial_capital < monthly_withdrawal:
            break
    return months, initial_capital

# Parameter
initial_capital = 10000000
monthly_withdrawal = 12000
annual_interest_rate = 1

# Berechnung
months, remaining_capital = calculate_months(initial_capital, monthly_withdrawal, annual_interest_rate)
print(f"\nDas Vermögen reicht für {months} Monate. Der Restwert beträgt {remaining_capital:.2f} €.")
