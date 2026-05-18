<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/OS%20Scheduling-Algorithms-0078D7?style=for-the-badge&logo=windows&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

# Enhancing Task Execution in multicore system-The impact of multilevel feedback queue on round robin adaptive priority scheduling algorithm

**CPU process scheduling simulator — FCFS, Round Robin & MLFQ implemented in Python**

[![GitHub](https://img.shields.io/badge/GitHub-kirana--23-181717?style=flat-square&logo=github)](https://github.com/kirana-23)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kirana--kira23-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/kirana-kira23)
[![Email](https://img.shields.io/badge/Email-kirana232004@gmail.com-D14836?style=flat-square&logo=gmail)](mailto:kirana232004@gmail.com)

</div>

---

## Overview

**Enhancing Task Execution** is a Python-based CPU process scheduling simulator that implements and compares three classic operating system scheduling algorithms. Each algorithm reads a set of processes from a CSV file and simulates their execution — reporting per-process metrics and overall CPU performance statistics.

The project is built with a clean object-oriented architecture: a shared `Base` class handles the core simulation loop, and each scheduling algorithm extends it by overriding only the relevant selection and burst logic.

---

## Scheduling Algorithms

### FCFS — First Come First Served (`fifo.py`)
Processes are executed in the order they arrive. Non-preemptive. Simple and fair, but can suffer from the convoy effect where short processes wait behind long ones.

### Round Robin (`round_robin.py`)
Each process is given a fixed **time quantum** in turn. If a process doesn't finish within its quantum, it goes back to the queue. Preemptive and fair — ideal for time-sharing systems.

| Queue Level | Time Quantum |
|-------------|-------------|
| User-defined | Entered at runtime via `input()` |

### MLFQ — Multi-Level Feedback Queue (`mlfq.py`)
Processes start in the highest-priority queue (Queue 0) with a short time quantum. If they don't finish, they're moved to a lower-priority queue with a longer quantum. I/O completion resets a process back to Queue 0.

| Queue Level | Time Quantum |
|-------------|-------------|
| Queue 0 | 4 units |
| Queue 1 | 16 units |
| Queue 2+ | Full remaining burst |

---

## Metrics Reported

After each simulation, the following are printed for every process and as averages:

| Metric | Description |
|--------|-------------|
| **Start–End** | Time the process began and finished execution |
| **Turnaround Time** | Total time from arrival to completion |
| **Response Time** | Time from arrival to first CPU allocation |
| **Waiting Time** | Time spent waiting in the ready queue |

**System-level metrics:**

| Metric | Description |
|--------|-------------|
| **Total Time** | Wall-clock time from start to last process completion |
| **Idle Time** | Time the CPU was idle waiting for processes to arrive |
| **CPU Utilization** | `(Total - Idle) / Total` |
| **Throughput** | Processes completed per unit time |

---

## Project Structure

```
enchancing-task-execution/
│
├── 🐍 base.py           # Core simulation engine — shared scheduling loop
├── 🐍 input_output.py   # CSV reader + formatted table output printer
├── 🐍 fifo.py           # FCFS (First Come First Served) scheduler
├── 🐍 round_robin.py    # Round Robin scheduler (time quantum via input)
├── 🐍 mlfq.py           # Multi-Level Feedback Queue scheduler
├── 🐍 cpu.py            # Combined runner / entry point
│
├── 📄 input.csv         # Sample process data (process_id, arrival, cpu1, io, cpu2)
└── 📄 README.md         # This file
```

### Architecture

```
Base (base.py)
├── FCFS        — overrides select() → earliest arrival_time
├── RoundRobin  — overrides select() + get_cpu_burst() → fixed time quantum
└── MLFQ        — overrides select(), get_cpu_burst(), on_cpu(), on_io() → feedback queues
```

---

## Input Format

Processes are defined in `input.csv` with the following columns:

```
process_id, arrival_time, cpu_time1, io_time, cpu_time2
```

| Column | Description |
|--------|-------------|
| `process_id` | Unique process identifier |
| `arrival_time` | Time the process enters the ready queue |
| `cpu_time1` | First CPU burst duration |
| `io_time` | I/O wait duration between the two CPU bursts |
| `cpu_time2` | Second CPU burst duration (0 if none) |

**Sample `input.csv`:**

```csv
process_id,arrival_time,cpu_time1,io_time,cpu_time2
1,3,4,0,0
2,4,6,0,0
3,2,5,0,0
4,1,3,0,0
5,0,4,0,0
6,2,3,0,0
```

---

## Getting Started

### Prerequisites

- Python 3.6 or higher
- No external dependencies — uses only the Python standard library

### Installation

```bash
git clone https://github.com/kirana-23/enchancing-task-execution.git
cd enchancing-task-execution
```

### Run FCFS

```bash
python fifo.py
```

### Run Round Robin

```bash
python round_robin.py
# Enter time quantum when prompted:
# > 4
```

### Run MLFQ

```bash
python mlfq.py
```

---

## Sample Output

```
P5: 0 -> 4
P4: 4 -> 7
P3: 7 -> 12
P6: 12 -> 15
P1: 15 -> 19
P2: 19 -> 25

+===================+===================+===================+===================+===================+
|                                       FCFS                                                        |
+===================+===================+===================+===================+===================+
|    Process ID     |     Start-End     |  Turn Around Time |   Response Time   |   Waiting Time    |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|        P1         |   15      -    19 |        16         |        12         |        12         |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|        P2         |   19      -    25 |        21         |        15         |        15         |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|      Average      |                   |       13.67       |        9.50       |        9.50       |
+-------------------+-------------------+-------------------+-------------------+-------------------+

Total Time: 25
Idle Time: 0
CPU Utilization: 1.00
Throughput: 0.24
```

---

## Concepts Covered

- Process scheduling and the ready queue
- Preemptive vs. non-preemptive scheduling
- CPU burst and I/O burst modeling
- Turnaround time, response time, and waiting time calculations
- CPU utilization and throughput as performance metrics
- Object-oriented design with inheritance and method overriding

---

## Author

**Kirana B**

[![GitHub](https://img.shields.io/badge/GitHub-kirana--23-181717?style=for-the-badge&logo=github)](https://github.com/kirana-23)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kirana--kira23-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/kirana-kira23)
[![Email](https://img.shields.io/badge/Email-kirana232004@gmail.com-D14836?style=for-the-badge&logo=gmail)](mailto:kirana232004@gmail.com)

---


<div align="center">
  <sub>for learning OS scheduling concepts and portfolio purposes</sub>
</div>
