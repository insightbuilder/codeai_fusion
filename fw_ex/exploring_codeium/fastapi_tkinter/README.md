# Python Problem Solver

## Overview
A desktop application that allows users to browse, solve, and save Python coding problems using FastAPI and Tkinter.

## Features
- List Python coding problems
- View problem descriptions
- Edit and write solutions in an integrated code editor
- Save solutions to local files

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository
2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the FastAPI backend:
   ```
   uvicorn main:app --reload
   ```
2. In a separate terminal, run the Tkinter frontend:
   ```
   python app.py
   ```

## Usage
- Select a problem from the list
- Read the problem description
- Write your solution in the code editor
- Click "Save Solution" to store your code

## Contributing
Feel free to submit issues and pull requests!

## License
MIT License
