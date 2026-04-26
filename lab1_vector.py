import threading, queue, time, random

class ProcessVector(threading.Thread):
    def __init__(self, pid, all_pids, peers):
        super().__init__(daemon=True)
        self.pid = pid
        self.clock = {p: 0 for p in all_pids} 
        self.inbox = queue.Queue()
        self.peers = peers

    def send(self, target_pid, message):
        self.clock[self.pid] += 1
        ts = dict(self.clock) # Copy state saat ini untuk dikirim
        print(f" [{self.pid}|VC={ts}] SEND '{message}' → {target_pid}")
        self.peers[target_pid].inbox.put((ts, self.pid, message))

    def receive(self):
        ts_sender, sender, msg = self.inbox.get()
        for p in self.clock:
            self.clock[p] = max(self.clock[p], ts_sender[p])
        self.clock[self.pid] += 1
        print(f" [{self.pid}|VC={self.clock}] RECV '{msg}' ← {sender}")

    def local_event(self, name):
        self.clock[self.pid] += 1
        print(f" [{self.pid}|VC={self.clock}] EVENT '{name}'")

    def run(self):
        time.sleep(random.uniform(0, 0.1))
        if self.pid == "P1":
            self.local_event("start")
            self.send("P2", "hello")
            self.receive() # Tunggu ack dari P2
        elif self.pid == "P2":
            self.receive() # Terima dari P1
            self.local_event("process")
            self.send("P1", "ack")
            self.send("P3", "data")
        elif self.pid == "P3":
            self.receive() # Terima dari P2
            self.local_event("done")

# List semua PID untuk inisialisasi vector
pids = ["P1", "P2", "P3"]
processes = {}
for pid in pids:
    processes[pid] = ProcessVector(pid, pids, processes)

print("=== Jalankan simulasi Vector Clock (Modifikasi Lab 1) ===")
for p in processes.values(): p.start()
for p in processes.values(): p.join(timeout=3)
print("=== Selesai ===")