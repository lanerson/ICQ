c1 = complex(input("digite um complexo [ex: 1+1j]: "))
c2 = complex(input("digite outro complexo [ex: 1-3j]: "))

print("|c1||c2| = |c1*c2|")
print(f"|c1||c2| = {abs(c1)*abs(c2)}")
print(f"|c1*c2| = {abs(c1*c2)}")
print("vale" if abs(c1)*abs(c2) == abs(c1*c2) else "não vale\n")
print("|c1 + c2| <= |c1| + |c2|")
print(f"|c1 + c2| = {abs(c1+c2)}")
print(f"|c1| + |c2| = {abs(c1)+abs(c2)}")
print("vale" if abs(c1+c2)<= abs(c1)+abs(c2) else "não vale\n")