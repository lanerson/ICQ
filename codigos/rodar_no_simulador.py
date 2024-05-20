from qiskit_ibm_runtime import QiskitRuntimeService
from get_token import get_token

token = get_token()

def rodar(circuit, token = token, resource = "ibm_brisbane"):
    service = QiskitRuntimeService(channel="ibm_quantum", 
                                token=token)
    QiskitRuntimeService.save_account(channel="ibm_quantum", 
                                    token=token,
                                    overwrite=True)
    from qiskit import transpile
    backend = service.backend(name = resource)
    qc_t = transpile(circuit, backend)
    backend.run(qc_t)

def rodar_simulador(circuit, token = token, resource = "ibmq_qasm_simulator"):
    service = QiskitRuntimeService(channel="ibm_quantum", 
                                token=token)    
    from qiskit import transpile
    backend = service.backend(name = resource)
    qc_t = transpile(circuit, backend)
    backend.run(qc_t)
