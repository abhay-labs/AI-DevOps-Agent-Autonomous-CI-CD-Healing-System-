import queue
import sys
sys.stdout.reconfigure(encoding="utf-8")

# ek queue banate hain jisme logs store honge
log_queue = queue.Queue()

def push_log(message):
    print(message)
    log_queue.put(message)

def stream_logs():
    while True:
        msg = log_queue.get()
        yield f"data: {msg}\n\n"
