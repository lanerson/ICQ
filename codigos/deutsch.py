from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from rodar_no_simulador import rodar
qubits = 2
input = 0
output = 1
zero = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])
one = Operator([
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0]
])
identity = Operator([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0]
])
negation = Operator([
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1]
])

def oracle(type):
    oracle = QuantumCircuit(qubits, name='oracle')
    oracle.append(type, range(qubits))
    return oracle

def deutsch(oracle):
    cbits = 1
    circuit = QuantumCircuit(qubits, cbits, name='deutsch')
    circuit.x(output)
    circuit.barrier()
    circuit.h(input)
    circuit.h(output)
    circuit.append(oracle.to_instruction(), range(qubits))
    circuit.h(input)
    circuit.barrier()
    circuit.measure(input, 0)
    return circuit

circuit = deutsch(oracle(zero))
circuit.draw(output='mpl')

rodar(circuit)
