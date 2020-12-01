# Performing Quantum State Tomography using Quantum Machine Learning: 
## Project Description: 
Quantum state tomography (QST) is a critical part of bench-marking quantum state preparation. We need to be sure that the quantum states we generate are what we expect them to be before we pass them onward into more complicated algorithms. It is also an important part of error analysis in order to build fault tolerant quantum computers.

There are many different approaches to quantum state tomography [1-5]. In this project we will explore a fairly new approach to quantum state tomography (proposed by Liu and colleagues [3]) which implements a variational quantum circuit (VQC) to reconstruct the unknown quantum states (article: arxiv.org/pdf/1912.07286). A summary of the method is provided here: 

We begin with an experimental process which prepares our target state $\ket{\psi}$ (this method is valid for mixed states as well but we consider pure states for simplicity). We produce an estimate state $\ket{\phi}$ via the variational quantum circuit. At this point the estimated state is generated through a randomized initialization of the parameters of the VQC (we denote the set of parameters as a vector: $\Vec{\theta}$). The fidelity between the two states is computed physically via a SWAP test. This quantity is used to optimize $\Vec{\theta}$ which in turn produces a better estimate state $\ket{\phi}$. Refer to figure 1 for a visual depiction of this framework as well as the specific ansatz used for the variational circuit.

## Results: 


## Future Direction: 


## References: 
1.  J. Rehacek, Z. Hradil, and M. Jezek, “Iterative algorithm for recon-struction of entangled states,” arXiv.org, Oct 2000.
2.  J. Carrasquilla, G. Torlai, R. G. Melko, and L. Aolita, “Reconstructing quantum states with generative models,” arXiv.org, Jul 2019.
3.  Y.  Liu,  D.  Wang,  S.  Xue,  A.  Huang,  X.  Fu,  X.  Qiang,  P.  Xu,  H.-L.Huang, M. Deng, C. Guo, and et al., “Variational quantum circuits for quantum state tomography,” arXiv.org, Apr 2020.
4.  G.  Torlai,  G.  Mazzola,  J.  Carrasquilla,  M.  Troyer,  R.  Melko,  andG.  Carleo,  “Neural-network  quantum  state  tomography,” NatureNews, Feb 2018.
5.  B.  Qi,  Z.  Hou,  L.  Li,  D.  Dong,  G.  Xiang,  and  G.  Guo,  “Quantumstate tomography via linear regression estimation,” arXiv.org, Dec2013.

# Code: 
The code for this project is split up into 4 sections: 

## Data Generation: 

## VQC based QST (original approach): 

## Current Research: 

## Visualization:

# Installation: 
## Installation for ML Models:
pip install --user -r requirements.txt

## Installation for Backend
pip install --user -r backend/requirements.txt

## Installation for Frontend
Check web/README.md.

# Live Demo
http://quantumstatetomography.sharankov.com/

# Acknowledgements:
