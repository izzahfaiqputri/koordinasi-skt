from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock
import threading, time

def worker(worker_id):
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    lock = Lock(zk, "/myapp/lock")
    print(f"[Worker-{worker_id}] Mencoba acquire lock...")
    with lock:
        print(f"[Worker-{worker_id}] Lock diperoleh! Masuk CR.")
        if worker_id == 1: raise Exception("Crash di tengah CR!") # MODIFIKASI --> Crash hanya terjadi pada worker 1
        time.sleep(2)
        print(f"[Worker-{worker_id}] Selesai, release lock.")
    zk.stop()

# threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)] # MODIFIKASI --> Mengubah range(3) menjadi range(5)
for t in threads: t.start()
for t in threads: t.join()
print("Semua worker selesai!")