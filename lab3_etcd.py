import etcd3
import threading
import time

def watch_key(etcd_client, key):
    """Watch sebuah key dan print setiap perubahan."""
    print(f"Watching key: {key}")
    events_iterator, cancel = etcd_client.watch(key)
    for event in events_iterator:
        print(f" Event: {type(event).__name__} | "
              f"key={event.key.decode()} | "
              f"value={event.value.decode() if event.value else 'deleted'}")

def node_candidate(node_id):
    """Fungsi simulasi untuk Leader Election Manual"""
    client = etcd3.client(host='localhost', port=2379)
    print(f"[{node_id}] Mencoba menjadi leader (campaign)...")
    
    while True:
        is_leader = client.put_if_not_exists('/election/leader', node_id)
        
        if is_leader:
            print(f"\n>>> [{node_id}] I am the leader! <<<")
            time.sleep(3)
            print(f"[{node_id}] Selesai bekerja, melepas jabatan (resign).\n")
            client.delete('/election/leader')
            break
        else:
            time.sleep(1)

etcd = etcd3.client(host='localhost', port=2379)
etcd.delete('/election/leader')

watcher_thread_1 = threading.Thread(
    target=watch_key, args=(etcd, b'/config/threshold'), daemon=True
)
watcher_thread_1.start()

# MODIFIKASI --> Tugas 1 start watcher untuk /config/timeout 
watcher_thread_2 = threading.Thread(
    target=watch_key, args=(etcd, b'/config/timeout'), daemon=True
)
watcher_thread_2.start()

time.sleep(0.5)
for i in range(3):
    value_thresh = f"threshold={80 + i}"
    value_time = f"timeout={100 + (i*10)}"
    etcd.put('/config/threshold', value_thresh)
    etcd.put('/config/timeout', value_time)
    print(f"Updated: {value_thresh} & {value_time}")
    time.sleep(1)

print("\n--- Leader Election dengan 2 Node ---")

# MODIFIKASI --> Tugas 2 leader election dengan 2 node
node1_thread = threading.Thread(target=node_candidate, args=("Node-1",))
node2_thread = threading.Thread(target=node_candidate, args=("Node-2",))

node1_thread.start()
node2_thread.start()

node1_thread.join()
node2_thread.join()

print("Semua simulasi selesai!")