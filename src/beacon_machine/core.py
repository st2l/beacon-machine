import os
import subprocess
import threading
import time

CISCO_OUI = (0x00, 0x40, 0x96)
RUN_SUFFIX_BASE = time.time_ns() & 0xFFFFFF


def generate_mac(index: int) -> str:
    suffix = (RUN_SUFFIX_BASE + index) & 0xFFFFFF
    b4 = (suffix >> 16) & 0xFF
    b5 = (suffix >> 8) & 0xFF
    b6 = suffix & 0xFF
    return f"{CISCO_OUI[0]:02x}:{CISCO_OUI[1]:02x}:{CISCO_OUI[2]:02x}:{b4:02x}:{b5:02x}:{b6:02x}"


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
