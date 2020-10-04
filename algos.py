from qiskit import IBMQ, BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
import matplotlib.pyplot as plt


def deutsch_jozsa(n=3, u="balanced"):
    """Function to simulate dz algo

    Args:
        n (int, optional): number of qubits. Defaults to 3.
        u (str, optional): balanced or constant oracle. Defaults to "balanced".
    """
    ins = QuantumRegister(n)
    aux = QuantumRegister(1)
    c = ClassicalRegister(n)

    circuit = QuantumCircuit(ins, aux, c)

    fig, ax = plt.subplots()
    # turning aux bin in (-) state
    circuit.x(aux)

    # inputs haddamard
    for i in [ins, aux]:
        circuit.h(i)

    # oracle
    if u == "balanced":
        circuit.barrier()
        circuit.cnot(ins[1], aux)
        circuit.barrier()
        ax.set_title("balanced")
    else:
        circuit.barrier()
        circuit.cnot(ins[0], aux)
        circuit.cnot(ins[0], aux)
        circuit.barrier()
        ax.set_title("constant")

    # output hadamard
    for i in [ins]:
        circuit.h(i)

    circuit.measure(ins, c)
    circuit.draw('mpl', ax=ax)

    backend = BasicAer.get_backend('qasm_simulator')
    shots = 1024
    results = execute(circuit, backend=backend, shots=shots).result()
    answer = results.get_counts()
    print("Simulator result")
    for c in answer:
        print(f"{c} is observed in {answer[c]} times")
    if c != str(0)*n:
        print("U is Balanced")
    else:
        print("U is Constant")
    plt.savefig("figs/dz.png", dpi=200)


def berstein_vazirani(n=3, b='100'):
    """berstein vazirani algorithm

    Args:
        n (int, optional): number of qubits. Defaults to 3.
        b (str, optional): linear bit to multiply to the input. Defaults to '100'.

    Raises:
        ValueError: [description]
    """
    fig, ax = plt.subplots()
    if len(b) != n:
        raise ValueError("len of bits must be equal to n")
    ins = QuantumRegister(n)
    aux = QuantumRegister(1)
    c = ClassicalRegister(n)

    circ = QuantumCircuit(ins, aux, c)

    # hadamard input
    circ.h(ins)
    # set aux to 1 and haddamard for (-)
    circ.x(aux)
    circ.h(aux)

    # U finction
    circ.barrier()
    b = b[::-1]
    for j, i in enumerate(b):
        if i == '1':
            circ.cnot(ins[j], aux)
        # else:circ.i(ins[j])
    circ.barrier()
    circ.h(ins)
    circ.measure(ins, c)
    circ.draw('mpl', ax=ax)

    backend = BasicAer.get_backend('qasm_simulator')
    shots = 1024
    results = execute(circ, backend=backend, shots=shots).result()
    answer = results.get_counts()
    for c in answer:
        print(f"{c} is observed in {answer[c]} times and the result is {c}")
    plt.savefig("figs/bz.png", dpi=200)


def simons(b='110'):
    """simons algorithm to solve for the secret bit

    Args:
        b (str, optional): secret bit to add to. Defaults to '110'.
    """
    fig, ax = plt.subplots()
    n = len(b)
    ins = QuantumRegister(n)
    aux = QuantumRegister(n)
    c = ClassicalRegister(n)

    circ = QuantumCircuit(ins, aux, c)

    # hadamard input
    circ.h(ins)

    # U finction oracle
    circ.barrier()
    b = b[::-1]
    circ.cnot(ins, aux)
    if '1' in b:
        i = b.find('1')
        for q in range(n):
            if b[q] == '1':
                circ.cx(ins[i], aux[q])
    circ.barrier()

    # hadamard to read
    circ.h(ins)
    circ.measure(ins, c)

    circ.draw('mpl', ax=ax)

    backend = BasicAer.get_backend('qasm_simulator')
    shots = 1024
    results = execute(circ, backend=backend, shots=shots).result()
    answer = results.get_counts()

    def bitxor(b, z):
        accum = 0
        for i in range(len(b)):
            accum += int(b[i]) * int(z[i])
        return (accum % 2)
    b = b[::-1]
    print('b = ' + b)
    for z in answer:
        print('{} b-xor {} = {} ({:.1f}%)'.format(b,
                                                  z, bitxor(b, z), answer[z]*100/shots))
    plt.savefig("figs/simon.png", dpi=200)
