import time
import secrets
import os
import threading

def generate_unique_code(splitter="-"):
    """
    Generate a highly unique code

    How Unique:

    1. `time.time_ns()` 
        - current timestamp in nanoseconds (19-digit number),
        - high-resolution, sortable base that almost always differs between calls.
    
    2. `os.getpid()` 
        - adds process-level entropy to avoid clashes between multiple processes
        - e.g., workers in a FastAPI/Gunicorn
    
    3. `threading.get_ident()` 
        - adds thread-level entropy to differentiate concurrent threads within same process.
    
    4. `secrets.randbelow(10_000)` 
        - adds 4-digit secure random padding to catch any edge cases

    """
    timestamp = time.time_ns()              
    pid = os.getpid()                      
    tid = threading.get_ident()           
    random_part = secrets.randbelow(10_000)

    base = f"{timestamp}{pid}{tid}{random_part:04d}"
    code = f"{base[0:4]}{splitter}{base[4:10]}{splitter}{base[10:16]}"
    return code




def create_vehicle_id():
    code = "VEH-{}".format(generate_unique_code())
    return code