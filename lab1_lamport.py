import threading, queue, time, random

class Process(threading.Thread):
    def __init__(self, pid, peers):
        super().__init__(daemon=True)
        self.pid = pid
        self.clock = 0
        self.inbox = queue.Queue()
        self.peers = peers 

    def send(self, target_pid, message):
        self.clock += 1
        ts = self.clock
        print(f" [{self.pid}|t={ts}] SEND '{message}' → {target_pid}")
        self.peers[target_pid].inbox.put((ts, self.pid, message))

    def receive(self):
        ts, sender, msg = self.inbox.get()
        self.clock = max(self.clock, ts) + 1
        print(f" [{self.pid}|t={self.clock}] RECV '{msg}' ← {sender}")

    def local_event(self, name):
        self.clock += 1
        print(f" [{self.pid}|t={self.clock}] EVENT '{name}'")

    def run(self):
        time.sleep(random.uniform(0, 0.2))
        if self.pid == "P1":
            self.local_event("start")
            self.send("P2", "hello")
            self.receive() # dari P2
        elif self.pid == "P2":
            self.receive() # dari P1
            self.local_event("process")
            self.send("P1", "ack")
            self.send("P3", "data")
        elif self.pid == "P3":
            self.receive() # dari P2
            self.local_event("done")
            # MODIFIKASI --> P3 kirim ke P4
            self.send("P4", "final_report")
        elif self.pid == "P4":
            # --- MODIFIKASI -->P4 menerima dari P3
            self.receive()
            self.local_event("archive")

processes = {}
# MODIFIKASI --> Tambah P4 di list pids
for pid in ["P1", "P2", "P3", "P4"]:
    processes[pid] = Process(pid, processes)

print("=== Jalankan simulasi Lamport Clock (P1, P2, P3, P4) ===")
for p in processes.values(): p.start()
for p in processes.values(): p.join(timeout=3)
print("=== Selesai ===")