import os
import subprocess
import threading
import time


def generate_mac(index: int) -> str:
    return f"00:14:24:{hex(index >> 16 & 0xff)[2:].zfill(2)}:{hex(index >> 8 & 0xff)[2:].zfill(2)}:{hex(index & 0xff)[2:].zfill(2)}"


def wait_for_input(stop_event: threading.Event) -> None:
    try:
        input("IF U WANNA STOP JUST PRESS ENTER\n")
    except (KeyboardInterrupt, EOFError):
        pass
    stop_event.set()


def launch_aps(interface: str, ssids: list[str], channel: int) -> None:
    processes = []
    print("-" * 60)

    devnull = open(os.devnull, "wb")

    for i, ssid in enumerate(ssids, start=1):
        mac = generate_mac(i)
        cmd = ["sudo", "airbase-ng", "-a", mac, "-e", ssid, "-c", str(channel), "-C", "25", "-X", interface]

        proc = subprocess.Popen(cmd, stdout=devnull, stderr=devnull, close_fds=True)
        processes.append(proc)

        print(f"[+] Deployed #{i}: SSID='{ssid}' | MAC=[{mac}] (PID: {proc.pid})\n")
        time.sleep(0.2)

    print("-" * 60)
    print(f"[*] All {len(ssids)} deployed")

    stop_event = threading.Event()
    input_thread = threading.Thread(target=wait_for_input, args=(stop_event,), daemon=True)
    input_thread.start()

    try:
        while not stop_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[-] Ctrl+C detected!")

    print("[-] Closing subprocesses, please wait...")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=0.2)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    devnull.close()
    print("All is cleared")
