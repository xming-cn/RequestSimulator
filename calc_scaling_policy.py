STANDARD_VALUE = 5.0
INCREASE_PERCENTAGE  = (0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8, 25.6)


increase_policy = []
decrease_policy = []

for v in INCREASE_PERCENTAGE:
    increase_point = v * STANDARD_VALUE + STANDARD_VALUE
    increase_policy.append(f'{v:>+6.0%} when RPT > {increase_point:>5.1f}')
    decrease_point = (1/(1+v)) * STANDARD_VALUE
    decrease_policy.append(f'{-(v/(1+v)):>6.0%} when RPT < {decrease_point:>5.1f}')

decrease_policy.reverse()
decrease_policy = decrease_policy[3:]

for policy in decrease_policy:
    print(f'{policy}')
print(f' Standard Value = {STANDARD_VALUE:>5.1f}')
for policy in increase_policy:
    print(f'{policy}')