<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/OS%20Scheduling-Algorithms-0078D7?style=for-the-badge&logo=windows&logoColor=white" />

# Enhancing Task Execution in multicore system with multi level feedback queue

**CPU process scheduling simulator — FCFS, Round Robin & MLFQ implemented in Python**

[![GitHub](https://img.shields.io/badge/GitHub-kirana--23-181717?style=flat-square&logo=github)](https://github.com/kirana-23)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kirana--kira23-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/kirana-kira23)
[![Email](https://img.shields.io/badge/Email-kirana232004@gmail.com-D14836?style=flat-square&logo=gmail)](mailto:kirana232004@gmail.com)

</div>

---

## Description

This project implements and simulates three classic CPU process scheduling algorithms in Python — **FCFS**, **Round Robin**, and **MLFQ** — built on a shared object-oriented base engine.

The core insight of the project is that **MLFQ is not a standalone algorithm but a combination of the other two**: Queue 0 and Queue 1 run Round Robin with increasing time quanta (4 and 16 units), while Queue 2+ runs FCFS giving the process its full remaining burst. Processes are demoted to lower queues when they exhaust their quantum (CPU-intensive behavior) and promoted back to Queue 0 when they return from I/O (interactive behavior).

The simulator reads process data from a CSV file and outputs per-process turnaround time, response time, and waiting time — along with system-wide CPU utilization and throughput.

---

## Scheduling Algorithms

### 1. FCFS — First Come First Served (`fifo.py`)

Non-preemptive. The process that arrives earliest gets the CPU first and runs to completion without interruption. Simple but can cause long waiting times if a large process arrives early (convoy effect).

### 2. Round Robin (`round_robin.py`)

Preemptive. Each process is given a fixed **time quantum** entered by the user at runtime. If a process doesn't finish within its quantum, it's put back in the ready queue with its `arrival_time` updated to the current time — so it re-enters in arrival order. This continues until all processes complete.

### 3. MLFQ — Multi-Level Feedback Queue (`mlfq.py`)

The most advanced algorithm — and the reason FCFS and Round Robin exist in this project. **MLFQ combines both algorithms across priority levels:**

| Queue | Algorithm Used | Time Quantum |
|-------|---------------|-------------|
| Queue 0 | **Round Robin** | 4 units |
| Queue 1 | **Round Robin** | 16 units |
| Queue 2+ | **FCFS** | Full remaining burst |

- **Queue 0 and Queue 1** use Round Robin logic — processes get a fixed time slice. If they don't finish, they're preempted and moved down.
- **Queue 2+** uses FCFS logic — `get_cpu_burst()` returns the full remaining burst, so the process runs to completion without interruption.

FCFS and Round Robin are not just separate algorithms here — **they are the building blocks that MLFQ is made of.**

---

## How MLFQ Works — Step by Step

Every process starts at **Queue 0** when it first arrives.

```
Process arrives → Queue 0 (RR, quantum = 4)
        │
        ├── Finishes cpu_time1 within 4 units?
        │       └── YES → goes to I/O → on_io() → queue resets to 0
        │                 returns from I/O → back to Queue 0 (promoted)
        │
        └── Still has cpu_time1 remaining after 4 units?
                └── NO  → on_cpu() → queue += 1 → demoted to Queue 1 (RR, quantum = 16)
                        │
                        ├── Finishes within 16 units?
                        │       └── YES → process ends
                        │
                        └── Still running after 16 units?
                                └── on_cpu() → queue += 1 → demoted to Queue 2+ (FCFS)
                                        └── runs full remaining burst to completion
```

### Selection Rule

At every scheduling decision, the ready process with the **lowest queue number** is picked. Ties are broken by **earliest arrival time**:

```python
def select(self, processes):
    return min(processes, key=lambda a: a['queue'] * 1000000 + a["arrival_time"])
```

Multiplying queue by `1,000,000` guarantees queue level always takes strict priority over arrival time.

### Demotion — `on_cpu()`

Called when a process **times out** (does not finish its burst within the quantum). Its queue level is incremented — lower priority, longer quantum next time:

```python
def on_cpu(self, process):
    process['queue'] += 1
```

### Promotion — `on_io()`

Called when a process **completes its first CPU burst** and enters I/O. It resets to Queue 0 when it returns — highest priority again, because it voluntarily gave up the CPU:

```python
def on_io(self, process):
    process['queue'] = 0
```

### Why This Design Works

| Process Type | Behavior | Result |
|-------------|----------|--------|
| Short / interactive | Finishes in Queue 0 or goes to I/O and resets | Always high priority, low wait |
| Medium CPU | Finishes in Queue 1 with longer quantum | Balanced priority |
| Heavy CPU-bound | Sinks to Queue 2+ and runs FCFS | Doesn't starve, just waits longer |

---

## Metrics Reported

Per-process metrics:

| Metric | Description |
|--------|-------------|
| **Start–End** | Time the process began and finished execution |
| **Turnaround Time** | Total time from arrival to completion |
| **Response Time** | Time from arrival to first CPU allocation |
| **Waiting Time** | Time spent waiting in the ready queue |

System-level metrics:

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
├── 🐍 fifo.py           # FCFS scheduler
├── 🐍 round_robin.py    # Round Robin scheduler (time quantum via input)
├── 🐍 mlfq.py           # MLFQ — combines FCFS + Round Robin across queues
├── 🐍 cpu.py            # Combined runner / entry point
│
├── 📄 input.csv         # Sample process data
└── 📄 README.md         # This file
```

### Class Architecture

```
Base (base.py)  ←  core run loop, timing, idle tracking, output
│
├── FCFS        — select(): earliest arrival_time
│
├── RoundRobin  — select(): earliest arrival_time
│                 get_cpu_burst(): fixed user-defined quantum
│
└── MLFQ        — select(): lowest queue → earliest arrival_time
                  get_cpu_burst(): 4 (Q0, RR) / 16 (Q1, RR) / full burst (Q2+, FCFS)
                  on_cpu(): queue += 1  → demotion on timeout
                  on_io():  queue  = 0  → promotion on I/O return
```

---

## Input Format

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
|        P2         |   18      -    24 |        20         |        14         |        14         |
+-------------------+-------------------+-------------------+-------------------+-------------------+
|      Average      |                   |       11.83       |        7.67       |        7.67       |
+-------------------+-------------------+-------------------+-------------------+-------------------+

Total Time: 24
Idle Time: 0
CPU Utilization: 1.00
Throughput: 0.25
```

---

## Concepts Covered

- CPU process scheduling and the ready queue
- Preemptive vs. non-preemptive scheduling
- How MLFQ unifies Round Robin and FCFS into a single adaptive algorithm
- CPU burst and I/O burst modeling
- Priority-based queue demotion and I/O-based promotion
- Turnaround time, response time, and waiting time
- CPU utilization and throughput
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
