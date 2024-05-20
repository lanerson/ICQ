from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService
 
qc = QuantumCircuit(2,2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0,1],[0,1])
qc.draw("mpl")
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel="ibm_quantum",token="45b044a0e68654e6c90becab5d2e679caff0e6ab5037a1498a884dd8460a85a9e50b92c29b4cbaf74dda9f413a605b902b518cdd2443eb4d244085c598578b54")
from qiskit import transpile
backend = service.backend(name = "simulator_statevector")
qc_t = transpile(qc, backend)
backend.run(qc_t)