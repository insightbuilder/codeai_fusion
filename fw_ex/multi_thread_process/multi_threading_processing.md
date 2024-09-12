In Python, both **multithreading** and **multiprocessing** are used to perform multiple tasks concurrently. However, they have key differences:

- **Multithreading**: Involves multiple threads running within the same process. Threads share the same memory space, which makes communication between threads easy but also introduces risks like race conditions.
- **Multiprocessing**: Involves multiple processes running independently. Each process has its own memory space, making it safer to work with but more expensive in terms of memory usage.

### 1. **Multithreading Example**

Multithreading in Python can be done using the `threading` module. Here's an example of multithreading where two threads print numbers concurrently.

```python
import threading
import time

# Function to print numbers
def print_numbers():
    for i in range(1, 6):
        print(f"Thread 1 - Number: {i}")
        time.sleep(1)

def print_letters():
    for letter in 'abcde':
        print(f"Thread 2 - Letter: {letter}")
        time.sleep(1)

# Create two threads
t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

# Start threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()

print("Both threads are done!")
```

In this example:

- **Two threads** are started: one to print numbers and another to print letters.
- They run concurrently and print their respective outputs.

### 2. **Multiprocessing Example**

Multiprocessing can be done using the `multiprocessing` module. Below is an example of running two processes concurrently.

```python
import multiprocessing
import time

# Function to print numbers
def print_numbers():
    for i in range(1, 6):
        print(f"Process 1 - Number: {i}")
        time.sleep(1)

def print_letters():
    for letter in 'abcde':
        print(f"Process 2 - Letter: {letter}")
        time.sleep(1)

if __name__ == '__main__':
    # Create two processes
    p1 = multiprocessing.Process(target=print_numbers)
    p2 = multiprocessing.Process(target=print_letters)

    # Start processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()

    print("Both processes are done!")
```

In this example:

- Two **separate processes** are created to print numbers and letters.
- Unlike threads, each process runs independently and doesn't share memory space.

### Key Differences:

1. **Multithreading**:
   
   - Good for I/O-bound tasks (e.g., reading files, network calls).
   - Threads share the same memory, so it's easy to share data between them but also riskier due to potential race conditions.
   - Limited by the Global Interpreter Lock (GIL) in Python, meaning true parallelism is not achieved for CPU-bound tasks.

2. **Multiprocessing**:
   
   - Better for CPU-bound tasks (e.g., heavy computations).
   - Each process has its own memory space, so there is no shared state, making it safer but more memory-intensive.
   - Multiprocessing achieves true parallelism because each process runs independently on different CPU cores.

### When to Use:

- **Multithreading**: Use when your task involves I/O operations (e.g., reading/writing files, network communication).
- **Multiprocessing**: Use when you need to perform CPU-bound tasks (e.g., processing large datasets, complex computations).
