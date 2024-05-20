from qiskit import QuantumCircuit

qc_a = QuantumCircuit(4)
qc_a.x(0)

qc_b = QuantumCircuit(2)
qc_b.y(0)
qc_b.z(1)


# compose qubists (0, 1) of qc_a
# to qubits (1, 3) of qc_b respectively
combined = qc_a.compose(qc_b, qubits=[3,2])

combined.draw("mpl", filename="combined.png")
