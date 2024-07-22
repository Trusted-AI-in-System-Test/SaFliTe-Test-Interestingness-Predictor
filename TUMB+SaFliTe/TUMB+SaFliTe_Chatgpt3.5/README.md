# TUMB at the SBFT 2024 Tool Competition - CPS-UAV Test Case Generation Track
## Overview
This is the implementation of our [UAV-Testing-Competition](https://github.com/skhatiri/UAV-Testing-Competition) tool called **TUMB** (**T**esting of **U**AVs by **M**CTS and Path **B**locking). Generally, it adopts the Monte Carlo Tree Search (MCTS) algorithm to place obstacles on the trajectories of Unmanned Aerial Vehicles (UAVs) to challenge its flight. A detailed description of the algorithm can be found [here](report/TUMB_UAVcompetition_SBFT2024.pdf).

## Getting Started

* Following [this guide](https://github.com/skhatiri/Aerialist#using-hosts-cli) to install Aerialist project

* Install Aerialist's python package:
     * `pip3 install git+https://github.com/skhatiri/Aerialist.git`
       
* `cd Aerialist/samples` and clone this project

* Create some necessary directories:
     * `cd UAV-Testing-Competition/snippets`
     * `sudo mkdir -p logs generated_tests results/logs`
 
* Run the experiment:
     * `python3 cli.py generate case_studies/mission1.yaml 100`

## Authors

* **Shuncheng Tang**
     * Email: scttt@mail.ustc.edu.cn
     * Affiliation: University of Science and Technology of China, China

* **Zhenya Zhang**
     * Email: zhang@ait.kyushu-u.ac.jp
     * Affiliation: Kyushu University, Japan

* **Ahmet Cetinkaya**
     * Email: ahmet@shibaura-it.ac.jp
     * Affiliation: Shibaura Institute of Technology, Japan
 
* **Paolo Arcaini**
     * Email: arcaini@nii.ac.jp
     * Affiliation: National Institute of Informatics, Japan
