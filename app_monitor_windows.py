import psutil
import time
import threading
from datetime import datetime
import csv
import os

def get_cpu_usage_single(pid, results):
    try:
        process = psutil.Process(pid)
        cpu_percent = process.cpu_percent(interval=1)
        results[pid] = cpu_percent
    except psutil.NoSuchProcess:
        print(f"Advertencia: No se encontró el proceso con PID {pid}.")
        results[pid] = 0.0
    except Exception as e:
        print(f"Error al obtener el uso de CPU para el PID {pid}: {e}")
        results[pid] = 0.0

def get_cpu_usage(pids, result_cpu):
    threads = []
    for pid in pids:
        thread = threading.Thread(target=get_cpu_usage_single, args=(pid, result_cpu))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result_cpu

def get_disk_io_rate_single(pid, results):
    try:
        process = psutil.Process(pid)

        io_counters = process.io_counters()
        read_bytes_start = io_counters.read_bytes
        write_bytes_start = io_counters.write_bytes

        time.sleep(1)

        io_counters = process.io_counters()
        read_bytes_end = io_counters.read_bytes
        write_bytes_end = io_counters.write_bytes

        read_rate = (read_bytes_end - read_bytes_start) / (1024 * 1024)
        write_rate = (write_bytes_end - write_bytes_start) / (1024 * 1024)
        results[pid] = (read_rate, write_rate)
    except psutil.NoSuchProcess:
        print(f"Advertencia: Proceso con PID {pid} no encontrado.")
        results[pid] = 0, 0
    except Exception as e:
        print(f"Error al obtener la velocidad de E/S de disco para el PID {pid}: {e}")
        results[pid] = 0, 0

def get_disk_io_rate(pids, result_disk):
    threads = []
    for pid in pids:
        thread = threading.Thread(target=get_disk_io_rate_single, args=(pid, result_disk))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result_disk

def get_network_io_rate_single(pid, results):
    try:
        process = psutil.Process(pid)

        net_io_counters_start = process.io_counters()
        bytes_sent_start = net_io_counters_start.write_bytes
        bytes_recv_start = net_io_counters_start.read_bytes

        time.sleep(1)

        net_io_counters_end = process.io_counters()
        bytes_sent_end = net_io_counters_end.write_bytes
        bytes_recv_end = net_io_counters_end.read_bytes

        sent_rate = (bytes_sent_end - bytes_sent_start) / (1024 * 1024)
        recv_rate = (bytes_recv_end - bytes_recv_start) / (1024 * 1024)
        results[pid] = (sent_rate, recv_rate)
    except psutil.NoSuchProcess:
        print(f"Advertencia: Proceso con PID {pid} no encontrado.")
        results[pid] = 0, 0
    except Exception as e:
        print(f"Error al obtener la velocidad de E/S de red para el PID {pid}: {e}")
        results[pid] = 0, 0

def get_network_io_rate(pids, result_network):
    threads = []
    for pid in pids:
        thread = threading.Thread(target=get_network_io_rate_single, args=(pid, result_network))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result_network

def get_all_results(pids):
    result_cpu = {}
    result_disk = {}
    result_network = {}
    
    cpu_thread = threading.Thread(target=get_cpu_usage, args=(pids, result_cpu))
    disk_thread = threading.Thread(target=get_disk_io_rate, args=(pids, result_disk))
    network_thread = threading.Thread(target=get_network_io_rate, args=(pids, result_network))
    
    cpu_thread.start()
    disk_thread.start()
    network_thread.start()

    cpu_thread.join()
    disk_thread.join()
    network_thread.join()

    return result_cpu, result_disk, result_network

def main():

    process_name = input("Ingresa el nombre de la aplicacion o proceso: ")
    contador = input("Ingrese la cantidad de registros que quiere realizar (cada registro toma un segundo): ")
    contador = int(contador)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_filepath = os.path.join(script_dir, f"{process_name}_monitor.csv")

    file = open(csv_filepath, mode="w", newline="")
    writer = csv.writer(file)
    writer.writerow(["Fecha", "CPU (%)", "RAM (MB)", "Escritura (MB/s)", "Lectura (MB/s)", "Internet Bajada (MB/s)", "Internet Subida (MB/s)"])

    while contador > 0:

        pids = [p.pid for p in psutil.process_iter() if process_name in p.name().lower()]

        if not pids:
            print(f"{process_name} no está en ejecución.")
            return

        total_ram = 0

        for pid in pids:
            try:
                process = psutil.Process(pid)
                memory_info = process.memory_info()
                pss_kb = memory_info.rss / 1024
                
                total_ram += pss_kb
            except psutil.NoSuchProcess:
                print(f"Advertencia: Proceso con PID {pid} no encontrado.")
                return 0
            except Exception as e:
                print(f"Error al obtener uso de RAM para el PID {pid}: {e}")
                return 0

        cpu_usages, disk_io_usages, network_io_usages = get_all_results(pids)

        total_cpu = sum(cpu_usages.values())
        num_cores = psutil.cpu_count(logical=True)
        average_cpu_usage = total_cpu / num_cores if num_cores else 0.0

        total_ram = total_ram / 1024

        total_read = 0
        total_write = 0
        for key, tupla in disk_io_usages.items():
            total_read += tupla[0]
            total_write += tupla[1]

        total_sent = 0
        total_recv = 0
        for key, tupla in network_io_usages.items():
            total_sent += tupla[0]
            total_recv += tupla[1]

        # print(f"{datetime.now().strftime("%H:%M:%S")} - Steam (Total) - CPU: {average_cpu_usage:.2f}% - RAM: {total_ram:.2f} MB - Disco R: {total_read:.2f} MB/s, W: {total_write:.2f} MB/s - Red In: {total_sent:.2f} MB/s, Out: {total_recv:.2f} MB/s")
        writer.writerow([datetime.now().strftime("%H:%M:%S"), f"{average_cpu_usage:.2f}", f"{total_ram:.2f}", f"{total_write:.2f}", f"{total_read:.2f}", f"{total_sent:.2f}", f"{total_recv:.2f}"])
        contador -= 1

    file.close()
    
if __name__ == "__main__":
    main()
