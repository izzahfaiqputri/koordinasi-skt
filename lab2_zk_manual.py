# lab2_zk_manual_lock.py
import threading, time
from kazoo.client import KazooClient

def worker(worker_id):
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    
    lock_path = "/myapp/manual_lock"
    zk.ensure_path(lock_path) 
    
    print(f"[Worker-{worker_id}] Mencoba acquire lock...")
    
    my_node_path = zk.create(f"{lock_path}/node-", ephemeral=True, sequence=True)
    my_node_name = my_node_path.split("/")[-1]
    
    acquired = False
    while not acquired:
        children = zk.get_children(lock_path)
        children.sort() 
        
        if children[0] == my_node_name:
            acquired = True
            print(f"[Worker-{worker_id}] Lock diperoleh! (Antrean: {my_node_name}) Masuk CR.")
        else:
            my_index = children.index(my_node_name)
            prev_node_name = children[my_index - 1]
            
            event = threading.Event()
            
            @zk.DataWatch(f"{lock_path}/{prev_node_name}")
            def watch_prev_node(data, stat, event_type):
                if event_type and event_type.type == "DELETED":
                    event.set()
                    return False
            
            print(f"[Worker-{worker_id}] Menunggu antrean {prev_node_name} selesai...")
            event.wait()
    
    time.sleep(2)
    print(f"[Worker-{worker_id}] Selesai, release lock. ({my_node_name})")
    
    zk.delete(my_node_path)
    zk.stop()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print("Semua worker selesai!")