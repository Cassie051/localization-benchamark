
# Indoor-Outdoor Robot Localization Benchmark

This repository contains the configuration files, launch scripts, and evaluation tools used in our comparative study on mobile robot localizations. The repository presents selected methods but could be extended for other algorithm allowing easy to comparition.

### Evaluated Algorithms
* **FAST-LIO2** (Tightly-coupled Iterated Kalman Filter)
* **GLIM** (Factor Graph Optimization with 3D Submaps)
* **RKO-LIO** (LiDAR-Inertial Odometry)
* **ORB-SLAM3** (Visual-Inertial Optimization)

### Dataset
This benchmark is pre-configured to run on the [Oxford Spires Dataset](https://dynamic.robots.ox.ac.uk/datasets/oxford-spires/).


## 📂 Repository Structure

```text
.
├── configs/                # Algorithm-specific parameter configurations
│   ├── fastlio/            
│   ├── glim/               
│   ├── orb_slam3/          
│   └── rko_lio/            
│
├── launch/                 # Custom ROS 2 launch files for running the algorithms
│   └── orb_slam3_launch.py 
│
├── scripts/                # Evaluation and automation tools
│   ├── benchmark_runner.py 
│   └── record_tum.py       
│
└── third_party/            # Submodules for the original algorithm source code
    ├── ros2_ws/            
    └── standalone/         

```


## ⚙️ Setup and Installation

### 1. Clone the Repository

Because the actual SLAM algorithms are linked as Git submodules inside the `third_party` folder, you **must** use the `--recursive` flag when cloning:

```bash
git clone --recursive https://github.com/Cassie051/localization-benchmark.git
cd localization-benchmark
```

### 2. Prerequisites

* **OS:** Ubuntu 24.04 (Recommended)
* **ROS:** ROS 2 Jazzy
* **Python Dependencies:** `evo` (for metric evaluation), `matplotlib`, `numpy`, `pandas`.

Install Python requirements:

```bash
pip install -r requirements.txt
```

### 3. Build the Algorithms

The algorithms are separated into ROS 2 packages and standalone CMake packages. You can build them using our provided setup script (if available in your root directory) or build them manually:

**For ROS 2 Packages (FAST-LIO2, RKO-LIO, etc.):**

```bash
source /opt/ros/jazzy/setup.bash
cd third_party/ros2_ws
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

**For Standalone Packages (ORB-SLAM3):**
Navigate into `third_party/standalone/orb_slam3` and follow the standard build instructions provided by the original authors (usually `./build.sh`).

### 4. Source the Environment

Before running any benchmark scripts, ensure you source both your ROS 2 installation and the compiled workspace:

```bash
source /opt/ros/jazzy/setup.bash
source third_party/ros2_ws/install/setup.bash
```

---

Because the updated `benchmark_runner.py` script is now a fully automated "batch runner" (it automatically iterates through all sequences, matches uncompressed bags for ORB-SLAM3, and executes all algorithms without needing command-line flags), the `Usage` section of the README needs to be simplified to reflect this powerful new workflow.

Here is the updated **Usage** section. You can copy and paste this to replace the `## 🚀 Usage` section in your `README.md`:


## 🚀 Usage

### 1. Data Preparation
Create a `datasets/` folder at the root of the repository. Place your ROS 2 bags inside. The script expects the baseline bags and any uncompressed variants (required for ORB-SLAM3) to be located in these directories.

### 2. Running the Benchmark Pipeline
The benchmarking process is fully automated. Simply run the main execution script from the root of the repository:

```bash
python3 scripts/benchmark_runner.py
```

*Note: The script will sequentially test all algorithms (GLIM, FAST-LIO2, ORB-SLAM3, KISS-ICP, and RKO-LIO) across all detected sequences. Generated TUM-format `.txt` trajectories are automatically saved into the `results/` folder, neatly organized by algorithm and sequence.*

### 3. Metric Evaluation & Plotting

Once the trajectories are populated in the `results/` folder.

**Metrics:** Saved TUM files allows to use the `evo` package to compute the Relative Pose Error (RPE) and Absolute Pose Error (APE) metrics.



## 📜 Citation

If you use this benchmark structure, configurations, or evaluation scripts in your research, please cite our paper:

```bibtex
@article{your_paper_id_2026,
  title={},
  author={},
  journal={},
  year={2026}
}
