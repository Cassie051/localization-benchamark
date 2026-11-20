
# Indoor-Outdoor Robot Localization Benchmark

This repository contains the configuration files, launch scripts, and evaluation tools used in our comparative study on mobile robot localizations. The repository presents selected methods but could be extended for other algorithm allowing easy to comparition.

### Evaluated Algorithms
* **FAST-LIO2** (Tightly-coupled Iterated Kalman Filter)
* **GLIM** (Factor Graph Optimization with 3D Submaps)
* **RKO-LIO** (LiDAR-Inertial Odometry)
* **ORB-SLAM3** (Visual-Inertial Optimization, monocular-inertial mode)
* **KISS-ICP** (LiDAR-only Point-to-Point ICP; no configuration file is needed, the LiDAR topic is remapped in `scripts/benchmark_runner.py`)
* **TSformer-VO** (learning-based monocular visual odometry; evaluated with the original implementation, see the paper)

### Dataset
This benchmark is pre-configured to run on the [Oxford Spires Dataset](https://dynamic.robots.ox.ac.uk/datasets/oxford-spires/).
The recordings do not contain a TF tree, so the IMU–LiDAR extrinsic is set explicitly in every configuration; all
configurations use the official Oxford Spires calibration.

The sequences `2024-03-18-christ-church-02` and `2024-03-20-christ-church-05` are split into Indoor, Outdoor and
Transition segments; the segment timestamps and the segmentation rule are given in [`segmentation/`](segmentation/README.md).


## 📂 Repository Structure

```text
.
├── configs/                # Algorithm-specific parameter configurations
│   ├── fastlio/            
│   ├── glim/               
│   ├── orb_slam3/          
│   └── rko_lio/            
│
├── segmentation/           # Indoor / Outdoor / Transition segment timestamps of the evaluated sequences
│   ├── crossings.csv
│   └── timestamps/
│
├── launch/                 # Custom ROS 2 launch files for running the algorithms
│   └── orb_slam3_launch.py 
│
├── scripts/                # Evaluation and automation tools
│   ├── benchmark_runner.py 
│   └── record_tum.py       
│
└── third_party/            # Submodules for the original algorithm source code
    ├── ros2_ws/src/        # ROS 2 packages
    │   ├── FAST_LIO_ROS2/  #   FAST-LIO2 (ROS 2 port)
    │   ├── glim/           #   GLIM
    │   ├── glim_ros2/      #   GLIM ROS 2 interface
    │   ├── kiss-icp/       #   KISS-ICP
    │   ├── rko_lio/        #   RKO-LIO
    │   └── orb_slam3_ros/  #   ORB-SLAM3 (ROS 2 wrapper)
    └── standalone/
        └── tsformer-vo-oxford-spires/   # TSformer-VO experiments

```


## ⚙️ Setup and Installation

### 1. Clone the Repository

Because the actual SLAM algorithms are linked as Git submodules inside the `third_party` folder, you **must** use the `--recursive` flag when cloning:

```bash
git clone --recursive https://github.com/Cassie051/localization-benchamark.git
cd localization-benchamark
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

**For ROS 2 Packages (FAST-LIO2, GLIM, KISS-ICP, RKO-LIO, ORB-SLAM3):**

```bash
source /opt/ros/jazzy/setup.bash
cd third_party/ros2_ws
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

Some packages have additional system dependencies (e.g. GTSAM and CUDA for the GPU version of GLIM, Pangolin and OpenCV for ORB-SLAM3); see the README of each package.

**For Standalone Packages (TSformer-VO):**
Follow the instructions in `third_party/standalone/tsformer-vo-oxford-spires`.

### 4. Source the Environment

Before running any benchmark scripts, ensure you source both your ROS 2 installation and the compiled workspace:

```bash
source /opt/ros/jazzy/setup.bash
source third_party/ros2_ws/install/setup.bash
```

---

## 🚀 Usage

### 1. Data Preparation
Create a `datasets/` folder at the root of the repository. Place your ROS 2 bags inside; to reproduce the paper, cut
the segments listed in `segmentation/timestamps/` from the original Oxford Spires recordings. The script expects the baseline bags and any uncompressed variants (required for ORB-SLAM3) to be located in these directories.

### 2. Running the Benchmark Pipeline
The benchmarking process is fully automated. Simply run the main execution script from the root of the repository:

```bash
python3 scripts/benchmark_runner.py
```

*Note: The script will sequentially test all algorithms (GLIM, FAST-LIO2, ORB-SLAM3, KISS-ICP, and RKO-LIO) across all detected sequences. Generated TUM-format `.txt` trajectories are automatically saved into the `results/` folder, neatly organized by algorithm and sequence.*

### 3. Metric Evaluation & Plotting

Once the trajectories are populated in the `results/` folder.

**Metrics:** Saved TUM files allows to use the `evo` package to compute the Relative Pose Error (RPE) and Absolute Pose Error (APE) metrics.



## ⚖️ License

The code and configuration files in this repository are released under the [MIT License](LICENSE)
(Copyright (c) 2026 Katarzyna Kijania and contributors).

* The files in `configs/fastlio/` and `configs/orb_slam3/` follow the configuration formats of
  [FAST-LIO2](https://github.com/hku-mars/FAST_LIO) (GPL-2.0) and [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3) (GPL-3.0).
  These programs are not included in this repository and remain under their own licenses.
* The segment timestamps in `segmentation/` are derived from the
  [Oxford Spires Dataset](https://dynamic.robots.ox.ac.uk/datasets/oxford-spires/) and are provided under the same license as the dataset,
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). If you use them, please also cite the Oxford Spires Dataset.
* Submodules in `third_party/` keep their own licenses.

## 📜 Citation

If you use this benchmark structure, configurations, segmentation, or evaluation scripts in your research, please cite our paper:

> K. Kijania, J. Dybała, P. Duszak, "A Comparative Study of Mobile Robot Localization Methods in Indoor–Outdoor Transition Scenarios", *Scientific Reports*, 2026 (under review).

```bibtex
@article{kijania2026indooroutdoor,
  title   = {A Comparative Study of Mobile Robot Localization Methods in Indoor--Outdoor Transition Scenarios},
  author  = {Kijania, Katarzyna and Dyba{\l}a, Jacek and Duszak, Piotr},
  journal = {Scientific Reports},
  year    = {2026},
  note    = {Under review}
}
```

Please also cite the [Oxford Spires Dataset](https://dynamic.robots.ox.ac.uk/datasets/oxford-spires/) and the original papers of the evaluated algorithms.
