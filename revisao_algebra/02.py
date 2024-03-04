print((1j)**15)


for num in range(1,16):
    print(f"i**{num} = {(1j)**num}")
"""
i**1 = 1j
i**2 = (-1+0j)
i**3 = (-0-1j)
i**4 = (1+0j)
i**5 = 1j
i**6 = (-1+0j)
i**7 = (-0-1j)
i**8 = (1+0j)
i**9 = 1j
i**10 = (-1+0j)
i**11 = (-0-1j)
i**12 = (1+0j)
i**13 = 1j
i**14 = (-1+0j)
i**15 = (-0-1j)
"""

def pot(num, exp):
    return num**(exp%4)

