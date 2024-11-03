# Diff Formats for Code Modifications

## Unified Diff
- **Description**: The most common format, showing a few lines of context around the changes. It uses `-` and `+` to indicate removed and added lines, respectively.
- **Usage**: Often used in version control systems like Git.

## Context Diff
- **Description**: Similar to unified diff but provides more context around the changes. It uses `!` to indicate changed lines, `-` for removed, and `+` for added lines.
- **Usage**: Useful for understanding changes in a broader context.

## Side-by-Side Diff
- **Description**: Displays changes in two columns, with the original file on the left and the modified file on the right.
- **Usage**: Useful for visually comparing changes side by side.

## Search/Replace Block
- **Description**: A structured format used to specify exact lines to search for and replace in a file.
- **Usage**: Useful for precise code modifications, ensuring exact matches and replacements.

# Thread Communication Problems and Solutions

## Problem 1: Race Condition
- **Description**: Occurs when two or more threads access shared data and try to change it at the same time.
- **Solution in Python**: Use locks (e.g., threading.Lock) to ensure that only one thread can access the shared data at a time.
- **Solution in Rust**: Use `std::sync::Mutex` or `std::sync::RwLock` to protect shared data, ensuring only one thread can access it at a time.

## Problem 2: Deadlock
- **Description**: Happens when two or more threads are blocked forever, each waiting on the other to release a lock.
- **Solution in Python**: Use a timeout for locks or a try-lock mechanism to avoid waiting indefinitely.
- **Solution in Rust**: Use `try_lock` methods provided by `Mutex` or `RwLock` to avoid indefinite waiting and detect potential deadlocks.

## Problem 3: Starvation
- **Description**: Occurs when a thread is perpetually denied access to resources it needs for execution.
- **Solution in Python**: Implement fair scheduling policies to ensure all threads get a chance to execute.
- **Solution in Rust**: Use fair locking mechanisms or design algorithms that ensure all threads have equal opportunity to access resources.

## Problem 4: Livelock
- **Description**: Similar to deadlock, but the states of the threads involved constantly change with regard to one another, none progressing.
- **Solution in Python**: Implement a back-off strategy or random delays to break the cycle of livelock.
- **Solution in Rust**: Use similar strategies as in Python, such as back-off algorithms or introducing randomness to break the cycle.

## Problem 5: Priority Inversion
- **Description**: Occurs when a lower-priority thread holds a lock needed by a higher-priority thread.
- **Solution in Python**: Use priority inheritance protocols to temporarily boost the priority of the lower-priority thread holding the lock.
- **Solution in Rust**: Implement priority inheritance manually or design systems to avoid priority inversion scenarios.
