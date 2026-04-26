class VectorClock:
    def __init__(self, pid, all_pids):
        self.pid = pid
        self.clock = {p: 0 for p in all_pids}

    def tick(self):
        """Mencatat kejadian internal (internal event)."""
        self.clock[self.pid] += 1
        return dict(self.clock)

    def send(self):
        """Mencatat persiapan pengiriman pesan (send event)."""
        self.clock[self.pid] += 1
        return dict(self.clock)

    def receive(self, remote_ts):
        """Sinkronisasi clock saat pesan diterima (receive event)."""
        for p in self.clock:
            self.clock[p] = max(self.clock[p], remote_ts[p])
        # Increment counter lokal sebagai tanda event penerimaan berhasil
        self.clock[self.pid] += 1 

    def happens_before(self, ts_a, ts_b) -> bool:
        """Memverifikasi apakah ts_a mendahului ts_b secara kausal."""
        leq = all(ts_a[p] <= ts_b[p] for p in ts_a)
        lt = any(ts_a[p] < ts_b[p] for p in ts_a)
        return leq and lt

    def concurrent(self, ts_a, ts_b) -> bool:
        """Mengecek apakah dua event tidak memiliki hubungan kausal (berjalan paralel)."""
        return (not self.happens_before(ts_a, ts_b) and
                not self.happens_before(ts_b, ts_a))

# SKENARIO
pids = ["P1", "P2", "P3"]
proc1 = VectorClock("P1", pids)
proc2 = VectorClock("P2", pids)
proc3 = VectorClock("P3", pids)

print("=== Tahap 1: Pengamatan Relasi Kausal ===")
# P1 melakukan inisiasi pengiriman
ts_1 = proc1.send() 
print(f"Event P1 (Kirim): {ts_1}")

# P2 menerima informasi dari P1, lalu mengirim pesan baru
proc2.receive(ts_1)
ts_2 = proc2.send()
print(f"Event P2 (Respon): {ts_2}")

print(f"Hasil Analisis Kausal (P1 -> P2): {proc1.happens_before(ts_1, ts_2)}")

print("\n=== Tahap 2: Pengamatan Event Konkuren (Paralel) ===")
# Skenario: P2 dan P3 bertindak tanpa saling mengetahui state satu sama lain
ts_concurrent_p2 = proc2.send()
ts_concurrent_p3 = proc3.send()

print(f"Timestamp P2 (Independen): {ts_concurrent_p2}")
print(f"Timestamp P3 (Independen): {ts_concurrent_p3}")

is_parallel = proc1.concurrent(ts_concurrent_p2, ts_concurrent_p3)
print(f"Apakah P2 dan P3 berjalan secara Konkuren? {is_parallel}")

print("\n=== Tahap 3: Penggabungan State di P1 ===")
# P1 menerima update dari dua sumber yang berbeda secara berurutan
print(f"Status Awal P1: {dict(proc1.clock)}")

proc1.receive(ts_concurrent_p2)
print(f"Status P1 setelah pesan dari P2: {dict(proc1.clock)}")

proc1.receive(ts_concurrent_p3)
print(f"Status P1 setelah pesan dari P3: {dict(proc1.clock)}")