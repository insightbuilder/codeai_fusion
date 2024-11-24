import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ServerReloader(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_server()

    def start_server(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        
        # First regenerate the gRPC stubs
        subprocess.run([
            sys.executable,
            '-m',
            'grpc_tools.protoc',
            '-I.',
            '--python_out=.',
            '--grpc_python_out=.',
            'store.proto'
        ])
        
        # Then start the server
        self.process = subprocess.Popen([sys.executable, 'server.py'])
        print("Server started")

    def on_modified(self, event):
        if event.src_path.endswith(('.py', '.proto')):
            print(f"Detected change in {event.src_path}")
            self.start_server()

def main():
    event_handler = ServerReloader()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    observer.join()

if __name__ == '__main__':
    main()
