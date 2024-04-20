import subprocess
import time
import sys

def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    if hours == 0:
        if minutes == 0:
            return f"{remaining_seconds} seconds"
        else:
            return f"{minutes} minutes and {remaining_seconds} seconds"
    else:
        return f"{hours} hours, {minutes} minutes, and {remaining_seconds} seconds"

start_time = time.time()

# Run the script and capture output
if len(sys.argv) < 2:
    print("Usage: python3 timing_script.py <file name to write output>")
outputFile = sys.argv[1] 
testing_file = 'cfr_tests.py'
result = subprocess.run(['python3', testing_file], capture_output=True, text=True)

end_time = time.time()

# Append output and errors to the existing file
with open(f"logs/{outputFile}", 'a') as f:
    f.write('\n--- New Execution Output ---\n')
    f.write(result.stdout)
    if result.stderr:
        f.write('\nErrors:\n')
        f.write(result.stderr)
    f.write(f"\nExecution time: {convert_seconds(end_time - start_time)}\n")

print(f"Program executed and output appended to '{outputFile}'.")