<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/OS%20Scheduling-Algorithms-0078D7?style=for-the-badge&logo=windows&logoColor=white" />

# Enhancing Task Execution in multicore system-the impact of MLFQ in round robin adaptive priority scheduling algorithm

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

### 1. FCFS — First Come First Served (`fifo.py`)

Non-preemptive. The process that arrives earliest gets the CPU first. Once a process starts, it runs to completion without interruption. Simple but can cause long waiting times if a large process arrives early.

### 2. Round Robin (`round_robin.py`)

Preemptive. Each process is given a fixed **time quantum** entered by the user at runtime. If a process doesn't finish within its quantum, it's put back in the ready queue with its `arrival_time` updated to the current time — so it re-enters the queue in arrival order. This continues until all processes complete.

### 3. MLFQ — Multi-Level Feedback Queue (`mlfq.py`)

The most advanced algorithm. Described in detail below.

---

## How MLFQ Works — In Detail

The Multi-Level Feedback Queue dynamically adjusts each process's priority based on its CPU usage behavior. Processes that use their full time quantum are penalized (moved to a lower-priority queue); processes that complete their CPU burst early or return from I/O are rewarded (reset to the highest-priority queue).

### Queue Structure

Every process starts at **Queue 0** (highest priority) when it first arrives.

| Queue | Time Quantum | Behavior |
|-------|-------------|----------|
| Queue 0 | 4 units | Short quantum — favors interactive/short processes |
| Queue 1 | 16 units | Longer quantum — for processes that needed more CPU |
| Queue 2+ | Full remaining burst | Non-preemptive — process runs to completion |

### Selection Rule

At every scheduling decision, the scheduler picks the process with the **lowest queue number**. If two processes are in the same queue, the one with the **earlier arrival time** wins. This is implemented as:

```python
def select(self, processes):
    return min(processes, key=lambda a: a['queue'] * 1000000 + a["arrival_time"])
```

Multiplying queue by `1,000,000` ensures queue level always takes priority over arrival time.

### Demotion — `on_cpu()`

If a process **does not finish** within its time quantum (i.e., `cpu_time1` is still > 0 after the burst), it is **demoted** — its queue number is incremented by 1:

```python
def on_cpu(self, process):
    process['queue'] += 1
```

This means the process used its full quantum without completing, indicating it is CPU-intensive. It gets a longer quantum next time but at lower priority.

### Promotion — `on_io()`

If a process **completes its first CPU burst** and goes to I/O (i.e., `cpu_time1` reaches 0 and `io_time` > 0), it is **reset to Queue 0** when it returns:

```python
def on_io(self, process):
    process['queue'] = 0
```

This rewards I/O-bound processes by treating them as high-priority again after they return from I/O — because they voluntarily gave up the CPU.

### Step-by-Step Execution Flow

```
Process arrives → assigned Queue 0
        │
        ▼
  Gets CPU for 4 units (Queue 0 quantum)
        │
        ├── Finishes cpu_time1? ──YES──► Goes to I/O → on_io() → queue = 0 (reset)
        │                                Returns from I/O → back to Queue 0
        │
        └── Still has cpu_time1? ─NO──► on_cpu() → queue += 1 (demoted to Queue 1)
                │
                ▼
        Gets CPU for 16 units (Queue 1 quantum)
                │
                ├── Finishes? ──YES──► Process ends
                │
                └── Still running? ──► on_cpu() → queue += 1 (demoted to Queue 2+)
                        │
                        ▼
                Gets full remaining burst (runs to completion)
```

### Why This Is Powerful

- **Short processes** finish quickly in Queue 0 — low waiting time
- **I/O-bound processes** keep resetting to Queue 0 — always high priority
- **CPU-intensive processes** gradually sink to lower queues — don't starve short ones
- **No starvation** — every process eventually gets CPU time in Queue 2+

---

## Metrics Reported

After each simulation, the following are printed per process and as averages:

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

### Class Architecture

```
Base (base.py)  ←  core run loop, timing, idle tracking, metrics
│
├── FCFS        — select(): picks earliest arrival_time
│
├── RoundRobin  — select(): picks earliest arrival_time
│                 get_cpu_burst(): returns fixed user-defined quantum
│
└── MLFQ        — select(): picks lowest queue, then earliest arrival_time
                  get_cpu_burst(): 4 (Q0) / 16 (Q1) / full burst (Q2+)
                  on_cpu(): queue += 1  (demote on timeout)
                  on_io():  queue  = 0  (promote on I/O completion)
```

---

## Input Format

Processes are defined in `input.csv` with the following columns:

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
P3: 7 -> 11
P6: 11 -> 14
P1: 14 -> 18
P2: 18 -> 22
P3: 22 -> 23

+===================+===================+===================+===================+===================+
|                                       MLFQ                                                        |
+===================+===================+===================+===================+===================+
|    Process ID     |     Start-End     |  Turn Around Time |   Response Time   |   Waiting Time    |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|        P1         |   14      -    18 |        15         |        11         |        11         |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|        P2         |   18      -    22 |        18         |        14         |        14         |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|      Average      |                   |       12.17       |        8.00       |        8.00       |
+-------------------+-------------------+-------------------+-------------------+-------------------+

Total Time: 23
Idle Time: 0
CPU Utilization: 1.00
Throughput: 0.26
```

---

## Concepts Covered

- Process scheduling and the ready queue
- Preemptive vs. non-preemptive scheduling
- CPU burst and I/O burst modeling
- Priority-based queue demotion and promotion
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
