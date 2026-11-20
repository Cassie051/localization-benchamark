#!/usr/bin/env python3

import subprocess
import time
import os
import signal
import glob
import shutil

# --- DYNAMIC REPOSITORY PATHS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

RESULTS_BASE_DIR = os.path.join(REPO_ROOT, "results")

BAGS_SOURCE_DIRS = [
    os.path.join(REPO_ROOT, "datasets", "2024-03-18-christ-church-02", "raw", "ros2bag", "multi_new"),
    os.path.join(REPO_ROOT, "datasets", "2024-03-20-christ-church-05", "raw", "ros2bag", "multi_new")
]

# --- ALGORITHM CONFIGURATIONS ---
ALGORITHMS = {
    "glim": {
        "cmd": f"ros2 run glim_ros glim_rosnode --ros-args -p config_path:={REPO_ROOT}/configs/glim",
        "needs_bag_play": True,
        "uses_tum_recorder": False, 
        "odom_topic": "", 
        "msg_type": "",
        "post_process": "glim" 
    },
    "fastlio": {
        "cmd": f"ros2 launch fast_lio mapping.launch.py config_file:={REPO_ROOT}/configs/fastlio/hesai.yaml",
        "needs_bag_play": True,
        "uses_tum_recorder": True,
        "odom_topic": "/Odometry",
        "msg_type": "Odometry",
        "post_process": None
    },
    "kiss_icp": {
        "cmd": "ros2 launch kiss_icp odometry.launch.py topic:=/hesai/pandar visualize:=false bagfile:={bag_path}",
        "needs_bag_play": False,
        "uses_tum_recorder": True,
        "odom_topic": "/kiss/odometry",
        "msg_type": "Odometry",
        "post_process": None
    },
    "orbslam": {
        "cmd": f"ros2 launch {REPO_ROOT}/launch/orb_slam3_launch.py",
        "needs_bag_play": True,
        "uses_tum_recorder": True,
        "odom_topic": "/camera_pose", 
        "msg_type": "PoseStamped", 
        "post_process": None
    },
    "rko_lio": {
        "cmd": f"ros2 launch rko_lio odometry.launch.py config_file:={REPO_ROOT}/configs/rko_lio/oxford_spires.yaml mode:=online dump_results:=false",
        "needs_bag_play": True,
        "uses_tum_recorder": True,
        "odom_topic": "/rko_lio/odometry",
        "msg_type": "Odometry",
        "post_process": None
    }
}

def get_sequence_name(bag_path):
    parts = bag_path.split(os.sep)
    try:
        idx = parts.index("datasets")
        return parts[idx + 1]
    except (ValueError, IndexError):
        return parts[-3] if len(parts) >= 3 else "unknown_sequence"

def find_rosbags_in_dirs(source_dirs):
    """Builds a dictionary with separate lists per sequence: { "sequence": {"base": [], "uncompressed": []} }"""
    sequences_data = {}
    
    for base_dir in source_dirs:
        if not os.path.exists(base_dir):
            print(f"[!] Warning: Source directory does not exist: {base_dir}")
            continue
            
        for item in os.listdir(base_dir):
            full_path = os.path.join(base_dir, item)
            if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "metadata.yaml")):
                seq_name = get_sequence_name(full_path)
                
                if seq_name not in sequences_data:
                    sequences_data[seq_name] = {"base": [], "uncompressed": []}
                
                if "uncompressed" in item.lower():
                    sequences_data[seq_name]["uncompressed"].append(full_path)
                else:
                    sequences_data[seq_name]["base"].append(full_path)
                
    for seq in sequences_data:
        sequences_data[seq]["base"].sort()
        sequences_data[seq]["uncompressed"].sort()
        
    return sequences_data

def handle_post_processing(algo_name, expected_output_file, algo_seq_dir, bag_name):
    if algo_name == "glim":
        direct_file = '/tmp/dump/traj_lidar.txt'
        if os.path.exists(direct_file):
            shutil.copy(direct_file, expected_output_file)
            print(f"  [+] Moved GLIM trajectory -> {expected_output_file}")
            os.remove(direct_file)
            return

        glim_dirs = [d for d in glob.glob('/tmp/dump/*') if os.path.isdir(d)]
        if glim_dirs:
            latest_dir = max(glim_dirs, key=os.path.getmtime)
            glim_file = os.path.join(latest_dir, 'traj_lidar.txt') 
            
            if os.path.exists(glim_file):
                shutil.copy(glim_file, expected_output_file)
                print(f"  [+] Moved GLIM trajectory -> {expected_output_file}")
                return
                
        print(f"  [!] Post-Process Error: traj_lidar.txt not found in /tmp/dump/")

def run_test(algo_name, target_bag_path, seq_name, clean_bag_name):
    config = ALGORITHMS[algo_name]
    
    print(f"\n=======================================================")
    print(f" SEQUENCE: {seq_name}")
    print(f" TESTING:  {algo_name.upper()} on BAG: {os.path.basename(target_bag_path)}")
    print(f" SAVING AS: {clean_bag_name}.txt")
    print(f"=======================================================")

    algo_seq_dir = os.path.join(RESULTS_BASE_DIR, algo_name, seq_name)
    os.makedirs(algo_seq_dir, exist_ok=True)
    tum_output_file = os.path.join(algo_seq_dir, f"{clean_bag_name}.txt")

    if algo_name == "glim":
        os.makedirs('/tmp/dump', exist_ok=True)

    algo_cmd = config['cmd'].format(bag_path=target_bag_path, results_dir=algo_seq_dir, bag_name=clean_bag_name)
    processes = []
    recorder_proc = None
    bag_proc = None

    try:
        if config.get('uses_tum_recorder', True):
            print(f"[1/3] Starting TUM recorder on {config['odom_topic']}...")
            recorder_cmd = f"python3 {SCRIPT_DIR}/record_tum.py {config['odom_topic']} {tum_output_file} {config['msg_type']}"
            recorder_proc = subprocess.Popen(recorder_cmd, shell=True, preexec_fn=os.setsid)
            processes.append(recorder_proc)
        else:
            print(f"[1/3] Skipping TUM recorder (Algorithm saves its own output).")

        print(f"[2/3] Launching {algo_name}...")
        algo_proc = subprocess.Popen(algo_cmd, shell=True, preexec_fn=os.setsid)
        
        wait_time =