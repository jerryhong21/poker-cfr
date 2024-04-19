import subprocess
import time

start_time = time.time()

# Run the script and capture output
testing_file = 'cfr_tests.py'
result = subprocess.run(['python3', testing_file], capture_output=True, text=True)

end_time = time.time()

# Append output and errors to the existing file
with open('logs/new_500m_regret_strategy_utility_timed.txt', 'a') as f:
    f.write('\n--- New Execution Output ---\n')
    f.write(result.stdout)
    if result.stderr:
        f.write('\nErrors:\n')
        f.write(result.stderr)
    f.write(f"\nExecution time: {end_time - start_time} seconds\n")

print("Program executed and output appended to 'output'.")