
import logging
from collections import namedtuple

import numpy as np
import numpy.random as rand
from qiskit.quantum_info import Pauli, Operator, PauliList


logger = logging.getLogger(__name__)

TspData = namedtuple('TspData', 'name dim coord w')


def calc_distance(coord, name='tmp'):
    assert coord.shape[1] == 2
    dim = coord.shape[0]
    w = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(i + 1, dim):
            delta = coord[i] - coord[j]
            w[i, j] = np.rint(np.hypot(delta[0], delta[1]))
    w += w.T
    return TspData(name=name, dim=dim, coord=coord, w=w)


def random_tsp(n, low=0, high=100, savefile=None, seed=None, name='tmp'):    
    assert n > 0
    if seed:
        rand.seed(seed)
    coord = rand.uniform(low, high, (n, 2))
    ins = calc_distance(coord, name)
    if savefile:
        with open(savefile, 'w') as outfile:
            outfile.write('NAME : {}\n'.format(ins.name))
            outfile.write('COMMENT : random data\n')
            outfile.write('TYPE : TSP\n')
            outfile.write('DIMENSION : {}\n'.format(ins.dim))
            outfile.write('EDGE_WEIGHT_TYPE : EUC_2D\n')
            outfile.write('NODE_COORD_SECTION\n')
            for i in range(ins.dim):
                x = ins.coord[i]
                outfile.write('{} {:.4f} {:.4f}\n'.format(i + 1, x[0], x[1]))
    return ins


def parse_tsplib_format(filename):    
    name = ''
    coord = None
    with open(filename) as infile:
        coord_section = False
        for line in infile:
            if line.startswith('NAME'):
                name = line.split(':')[1]
                name.strip()
            elif line.startswith('TYPE'):
                typ = line.split(':')[1]
                typ.strip()
                if typ != 'TSP':
                    logger.warning('This supports only "TSP" type. Actual: {}'.format(typ))
            elif line.startswith('DIMENSION'):
                dim = int(line.split(':')[1])
                coord = np.zeros((dim, 2))
            elif line.startswith('EDGE_WEIGHT_TYPE'):
                typ = line.split(':')[1]
                typ.strip()
                if typ != 'EUC_2D':
                    logger.warning('This supports only "EUC_2D" edge weight. Actual: {}'.format(typ))
            elif line.startswith('NODE_COORD_SECTION'):
                coord_section = True
            elif coord_section:
                v = line.split()
                index = int(v[0]) - 1
                coord[index][0] = float(v[1])
                coord[index][1] = float(v[2])
    return calc_distance(coord, name)


def get_tsp_qubitops(ins, penalty=1e5):
    num_nodes = ins.dim
    num_qubits = num_nodes ** 2
    zero = np.zeros(num_qubits, dtype=bool)
    pauli_list = []
    shift = 0
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                continue
            for p in range(num_nodes):
                q = (p + 1) % num_nodes
                shift += ins.w[i, j] / 4

                zp = np.zeros(num_qubits, dtype=bool)
                zp[i * num_nodes + p] = True                
                pauli_list.append([-ins.w[i, j] / 4, Pauli((zp, zero))])

                zp = np.zeros(num_qubits, dtype=bool)
                zp[j * num_nodes + q] = True
                pauli_list.append([-ins.w[i, j] / 4, Pauli((zp, zero))])

                zp = np.zeros(num_qubits, dtype=bool)
                zp[i * num_nodes + p] = True
                zp[j * num_nodes + q] = True
                
                pauli_list.append([ins.w[i, j] / 4, Pauli((zp, zero))])

    for i in range(num_nodes):
        for p in range(num_nodes):
            zp = np.zeros(num_qubits, dtype=bool)
            zp[i * num_nodes + p] = True
            pauli_list.append([penalty, Pauli((zp, zero))])
            shift += -penalty

    for p in range(num_nodes):
        for i in range(num_nodes):
            for j in range(i):
                shift += penalty / 2

                zp = np.zeros(num_qubits, dtype=bool)
                zp[i * num_nodes + p] = True
                pauli_list.append([-penalty / 2, Pauli((zp, zero))])

                zp = np.zeros(num_qubits, dtype=bool)
                zp[j * num_nodes + p] = True
                pauli_list.append([-penalty / 2, Pauli((zp, zero))])

                zp = np.zeros(num_qubits, dtype=bool)
                zp[i * num_nodes + p] = True
                zp[j * num_nodes + p] = True
                pauli_list.append([penalty / 2, Pauli((zp, zero))])

    for i in range(num_nodes):
        for p in range(num_nodes):
            for q in range(p):
                shift += penalty / 2

                zp = np.zeros(num_qubits, dtype=bool)
                zp[i * num_nodes + p] = True
                pauli_list.append([-penalty / 2, Pauli((zp, zero))])

                zp = np.zeros(num_qubits, dtype=bool)
                zp[i * num_nodes + q] = True
                pauli_list.append([-penalty / 2, Pauli((zp, zero))])

                zp = np.zeros(num_qubits, dtype=bool)
                zp[i * num_nodes + p] = True
                zp[i * num_nodes + q] = True
                pauli_list.append([penalty / 2, Pauli((zp, zero))])
    shift += 2 * penalty * num_nodes   
    
    return Operator(pauli_list), shift

# Implementação
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

qc = create_qaoa_circuit(initial_params, qubo, 3)
qc.draw()