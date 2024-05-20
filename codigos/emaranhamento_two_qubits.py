from qiskit import QuantumCircuit

qc = QuantumCircuit(2,2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()


# qc.draw("mpl", filename="emaranhamento_two_qubits.png")
from rodar_no_simulador import rodar_simulador

rodar_simulador(qc)