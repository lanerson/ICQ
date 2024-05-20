def guess(f):
    constant = 0
    balanced = 1

    if f(0) == 0:
        if f(1) == 0:
            return constant # zero
        elif f(1) == 1:
            return balanced # identity
    elif f(0) == 1:
        if f(1) == 0:
            return balanced # negation
        elif f(1) == 1:
            return constant # one
        
def zero(bit):
    return 0

def one(bit):
    return 1

def identity(bit):
    return bit

def negation(bit):
    return 1 - bit

def test_guess(name, type):
    print(name, 'is', 'constant' if guess(type) == 0 else 'balanced')

test_guess('Zero', zero)
test_guess('One', one)
test_guess('Identity', identity)
test_guess('Negation', negation)

