import csv


def read_input(input_file):
    processes = []
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                processes.append({"process_id": int(row[0]),
                                  "arrival_time": int(row[1]),
                                  "cpu_time1": int(row[2]),
                                  "io_time": int(row[3]),
                                  "cpu_time2": int(row[4])}
                                 )
            line_count += 1
    return processes


def tab(s, n=19, d='c'):
    if s is not str:
        if type(s) is float:
            s = "{:.2f}".format(s)
        else:
            s = str(s)
    l = len(s)
    if d == 'l':
        return s + " " * (n - l)
    elif d == 'c':
        return (n - l - (n - l) // 2) * " " + s + ((n - l) // 2) * " "
    elif d == 'r':
        return " " * (n - l) + s


def print_output(title, processes, total_time=0, idle_time=0):
    print()
    t = ("+" + "=" * 19) * 5 + '+'
    t2 = ("+" + "-" * 19) * 5 + '+'
    l = len(t)
    print(t)
    print(f'''|{tab(title, l - 2, "c")}|''')
    print(t)
    print(
        f'''|{tab("Process ID")}|{tab("Start-End")}|{tab("Turn Around Time")}|{tab("Response Time")}|{tab("Waiting Time")}|''')
    print(t2)

    for p in processes:
        print(
            f'''|{tab("P" + tab(p["process_id"], 0))}|{tab(tab(p["start"], 3, 'l') + '-' + tab(p["end"], 3, 'r'))}|{tab(p["turn_around_time"])}|{tab(p["response_time"])}|{tab(p["waiting_time"])}|''')

        print(t2)

    print(f'''|{tab("Average",39)}|{tab(sum([p["turn_around_time"] for p in processes]) / len(processes)):}|{tab(sum([p["response_time"] for p in processes]) / len(processes))}|{tab(sum([p["waiting_time"] for p in processes]) / len(processes))}|''')
    print(t2[:20] + '-' + t2[21:])
    print()
    print(f'Total Time: {total_time}')
    print(f'Idle Time: {idle_time}')
    print(f'CPU Utilization: {((total_time - idle_time) / total_time):.2f}')
    print(f'Throughput: {(len(processes)/ total_time):.2f}')


def get_instance(pid="", start="", end="", turn_around_time="", response_time="", waiting_time=""):
    return {"process_id": pid,
            "start": start,
            "end": end,
            "turn_around_time": turn_around_time,
            "response_time": response_time,
            "waiting_time": waiting_time
            }
from input_output import *


class Base:
    def __init__(self, processes, title="RoundRobin"):
        self.procs = {}
        for p in processes:
            self.procs[p["process_id"]] = get_instance(p["process_id"], start=-1, waiting_time=0, turn_around_time=0)
            self.procs[p["process_id"]].update(**p)
            self.procs[p["process_id"]]["is_ended"] = False
            self.procs[p["process_id"]]["a_b"] = self.procs[p["process_id"]]["arrival_time"]
        self.t = 0
        self.q = 1
        self.idle = 0
        self.title = title

    def select(self, processes):
        return processes[0]

    def run(self):
        p_old = None
        s = 0
        while True:
            ps = [i for i in self.procs.values() if not i["is_ended"] and i["arrival_time"] <= self.t]
            if ps:
                p = self.select(ps)
            else:
                ps = [i for i in self.procs.values() if not i["is_ended"]]
                if ps:
                    p = min(ps, key=lambda a: a["arrival_time"])
                else:
                    break
            if p_old is not None and p_old != p:
                pass
                # print(f'P{p_old["process_id"]}: {s} -> {self.t}, queue: {p_old["queue"]}')
            if self.t < p["arrival_time"]:
                self.idle += p["arrival_time"] - self.t
                self.t = p["arrival_time"]
            else:
                p["waiting_time"] += self.t - p["arrival_time"]
            # if p_old is None or p_old != p:
            s = self.t
            self.q = self.get_cpu_burst(p)
            if self.q > p["cpu_time1"]:
                exe = p["cpu_time1"]
            else:
                exe = self.q
            if p["start"] == -1:
                p["start"] = self.t
                p["response_time"] = p["start"] - p["arrival_time"]
            if p["cpu_time1"]:
                self.t += exe
                p["cpu_time1"] -= exe
                if p["cpu_time1"]:
                    p["arrival_time"] = self.t
                    self.on_cpu(p)
                else:
                    p["arrival_time"] = self.t + p["io_time"]
                    self.on_io(p)
                    if not p["cpu_time2"]:
                        p["end"] = self.t
                        p["turn_around_time"] = p["end"] - p["a_b"]
                        p["is_ended"] = True
            else:
                if self.q > p["cpu_time2"]:
                    exe = p["cpu_time2"]
                else:
                    exe = self.q
                self.t += exe
                p["cpu_time2"] -= exe
                if p["cpu_time2"]:
                    p["arrival_time"] = self.t
                    self.on_cpu(p)
                else:
                    p["end"] = self.t
                    p["turn_around_time"] = p["end"] - p["a_b"]
                    p["is_ended"] = True
            p_old = p
            print(f'P{p_old["process_id"]}: {s} -> {self.t}')

    def show(self):
        self.run()
        print_output(self.title, self.procs.values(), total_time=self.t, idle_time=self.idle)

    def on_io(self, process):
        pass

    def on_cpu(self, process):
        pass

    def get_cpu_burst(self, process):
        return self.cpu_burst_proc(process)

    def cpu_burst_proc(self, process):
        if process["cpu_time1"]:
            return process["cpu_time1"]
        else:
            return process["cpu_time2"]



from input_output import read_input
from base import Base


class RoundRobin(Base):
    def __init__(self, processes, time_quantum):
        super(RoundRobin, self).__init__(processes, "RoundRobin")
        self.q = time_quantum

    def select(self, processes):
        return min(processes, key=lambda a: a["arrival_time"])

    def get_cpu_burst(self, process):
        return self.q


RoundRobin(read_input('input.csv'), int(input())).show()


from input_output import read_input
from base import Base


class RoundRobin(Base):
    def __init__(self, processes, time_quantum):
        super(RoundRobin, self).__init__(processes, "RoundRobin")
        self.q = time_quantum

    def select(self, processes):
        return min(processes, key=lambda a: a["arrival_time"])

    def get_cpu_burst(self, process):
        return self.q


RoundRobin(read_input('input.csv'), int(input())).show()

from input_output import read_input
from base import Base


class MLFQ(Base):
    def __init__(self, processes):
        for p in processes:
            p["queue"] = 0
        super(MLFQ, self).__init__(processes, title="MLFQ")

    def select(self, processes):
        return min(processes, key=lambda a: a['queue'] * 1000000 + a["arrival_time"])

    def on_cpu(self, process):
        process['queue'] += 1

    def on_io(self, process):
        process['queue'] = 0

    def get_cpu_burst(self, process):
        if process['queue'] == 0:
            return 4
        elif process['queue'] == 1:
            return 16
        else:
            return self.cpu_burst_proc(process)


MLFQ(read_input('input.csv')).show()

