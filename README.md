# Performing Quantum State Tomography using Quantum Machine Learning: 
## Project Description: 
Quantum state tomography (QST) is a critical part of bench-marking quantum state preparation. We need to be sure that the quantum states we generate are what we expect them to be before we pass them onward into more complicated algorithms. It is also an important part of error analysis in order to build fault tolerant quantum computers.

There are many different approaches to quantum state tomography [1-5]. In this project we will explore a fairly new approach to quantum state tomography (proposed by Liu and colleagues [3]) which implements a variational quantum circuit (VQC) to reconstruct the unknown quantum states ([original paper](https://arxiv.org/pdf/1912.07286.pdf)). A summary of the method is provided here: 

We begin with an experimental process which prepares our target state (this method is valid for mixed states as well but we consider pure states for simplicity). We produce an estimate state via the variational quantum circuit (VQC). At this point the estimated state is generated through a randomized initialization of the parameters of the VQC. The fidelity between the two states is computed physically via a SWAP test. This quantity is used to optimize the parameterization vector which in turn produces a better estimate state. Refer to figure 1 for a visual depiction of this framework as well as the specific ansatz used for the variational circuit (this diagram was taken from the [3]).

<img src="/images/setup_framework.PNG" width="400" height="500">

**Figure 1**: QML architecture


## Results: 
A (5 qubit) quantum state was randomly generated to act as our unknown target state to be reconstructed. We began by varying the the depth of the VQC and plotting 1 - Fidelity between the target state and the estimate state to determine the relation ship between circuit depth and accuracy of reconstruction (summarized in figure 2a). We then fixed the circuit depth to 10 layers and plotted the loss function over each iteration to see how quickly we were able to converge to the unknown target state (summarized in figure 2b). Similar metrics were computed in the original paper and their results are summarized in figure 3 (taken from [3]). We see that the two sets of graphs agree well with eachother, thus we have successfully replicated the method described in the paper.  

<img src="/images/our_results.PNG" width="500" height="250">

**Figure 2**: a) reproduced results for measuring the difference between the target <br/> 
state and the estimated state as we vary the circuit depth. b) reproduced results for <br/> 
measuring the loss function over the number of optimization iterations.

<img src="/images/Main_results_new.PNG" width="500" height="250">

**Figure 3** : results as described in the original paper [3]. 

## Future Direction: 
Once we have optimized our VQC parameterization, our estimate state will be identical to our target state. In order to explicitly reconstruct the target state we would need to implement our VQC on a classical simulator along with our tuned parameterization. The simulation would produce the complex coefficients that describe our reconstructed state vector.

The classical simulation process scales with time complexity O(2^N) and new simulations must be done each time we attempt to reconstruct a new target state. We identified this as a bottle neck in the overall process of VQC based QST. We postulate that a machine learning model could potentially learn the association between a parameterization of the VQC and its associated quantum state. If this was possible, one could train a model for a variational circuit (with a fixed circuit depth) a priori and use it instead of running the classical quantum circuit simulator. Since the parameters of the VQC scale with polynomial time complexity (O(N^3 d^2)) this supervised model would run more efficiently than explicitly learning the quantum states.

Currently, we are exploring classical machine learning approaches in order to accomplish this. 

## References: 
* [1]  J. Rehacek, Z. Hradil, and M. Jezek, “Iterative algorithm for recon-struction of entangled states,” arXiv.org, Oct 2000.
* [2]  J. Carrasquilla, G. Torlai, R. G. Melko, and L. Aolita, “Reconstructing quantum states with generative models,” arXiv.org, Jul 2019.
* [3]  Y.  Liu,  D.  Wang,  S.  Xue,  A.  Huang,  X.  Fu,  X.  Qiang,  P.  Xu,  H.-L.Huang, M. Deng, C. Guo, and et al., “Variational quantum circuits for quantum state tomography,” arXiv.org, Apr 2020.
* [4]  G.  Torlai,  G.  Mazzola,  J.  Carrasquilla,  M.  Troyer,  R.  Melko,  andG.  Carleo,  “Neural-network  quantum  state  tomography,” NatureNews, Feb 2018.
* [5]  B.  Qi,  Z.  Hou,  L.  Li,  D.  Dong,  G.  Xiang,  and  G.  Guo,  “Quantumstate tomography via linear regression estimation,” arXiv.org, Dec2013.

# Code: 
The code for this project is split up into 3 sections: 

* **VQC based QST (original approach)**: 
  In the folder `qml_approach` we recreated the method as described in [3]. Please reference the jupyter notebook to see how we reproduced the results. 
  
* **Current Research**:
  In the folder `wrapped_qml_method` we are exploring classical ML methods to make VQC based QST more efficient. 

* **Visualization**:
  (insert description here)

# Meet the Team: 
**Jay Soni** *(Quantum Computing Lead)*: A Mathematical Physics major with a passion for quantum computing. Enjoys coding almost as much as he enjoys drinking Ice Capps! 

**Ivan Sharankov** *(Machine Learning Lead)*: Astrophysics major who's looking to continue his masters in computational physics. I love programming and will jump on any hackathon or project I can find. Interested in handling big science data, machine learning applications in physics, cryptogtaphy, and network engineering.

**Kar Lok Ng** *(Statistician)*: An ex-Physics major currently in Mathematics, with the goal of majoring in Statistics. Currently throwing himself at ML and seeing what happens.

**Kevin Bacabac** *(Full Stack Developer)*: A Computer Science major who loves game dev. "Any data can look nice as a spinning rainbow."

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
We would like to acknowledge the team at **Schrodinger Hacks** for organizing the event and motivating this project. We would like to thank Mr.Prashil Gandhi for his technical insights on the implementation of the project. Finally, we would like to give a big thanks to Mr. Mohamed Hibat Allah; without his mentorship and guidance this project would not be complete. 

If you have any questions about this project feel free to reach out to me at jbsoni@uwaterloo.ca
