import numpy as np
import qiskit
from qiskit_textbook.widgets import plot_bloch_vector_spherical
from qiskit.visualization import plot_bloch_multivector


import visualizer

def show_radial(coords):
  plt = plot_bloch_vector_spherical(coords)
  return visualizer._export_png(plt)


def show_multivector(coords):
  qc = qiskit.QuantumCircuit(1)

  non_normalized = np.array([complex(*coords[0:2]), complex(*coords[2:4])])
  # Normalize each component
  part_normalized = np.nan_to_num(non_normalized / np.abs(non_normalized))  # nan -> 0

  # Normalize all components
  initial_state = part_normalized / np.linalg.norm(part_normalized)

  qc.initialize(initial_state, 0)

  backend = qiskit.Aer.get_backend('statevector_simulator')
  out = qiskit.execute(qc, backend).result().get_statevector()
  plt = plot_bloch_multivector(out)
  return visualizer._export_png(plt)
