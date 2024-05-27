import numpy as np
from qiskit import QuantumCircuit
import tsp
from scipy.optimize import minimize

# Define o problema do TSP
num_cities = 3  # Número de cidades
ins = tsp.random_tsp(num_cities)
qubo, offset = tsp.get_tsp_qubitops(ins)
num_qubits = qubo.num_qubits

# Função para construir o circuito QAOA
def create_qaoa_circuit(params, qubo, p):
    beta = params[:p]
    gamma = params[p:]
    
    qc = QuantumCircuit(num_qubits)
    
    # Estado inicial |+>^n
    for i in range(num_qubits):
        qc.h(i)
    
    for i in range(p):
        # Aplica U(C, gamma)
        for pauli in qubo.paulis:
            weight = pauli[0]
            term = pauli[1]
            qc.rz(2 * gamma[i] * weight, term)
        
        # Aplica U(B, beta)
        for qubit in range(num_qubits):
            qc.rx(2 * beta[i], qubit)
    
    return qc

# Otimização dos parâmetros
p = 1  # Número de camadas
initial_params = np.random.uniform(0, 2*np.pi, 2*p)
