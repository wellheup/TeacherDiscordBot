#!/bin/bash

echo "Starting test run with a timeout of 60 seconds..."

# Run pytest with a timeout and redirect output to a log file for future reference
timeout 60s pytest --maxfail=1 2>&1 | tee result.log

# Capture the exit code of pytest for debugging purposes
EXIT_CODE=${PIPESTATUS[0]}
echo "Exit code of pytest: $EXIT_CODE"

# Wait for pytest to finish running before proceeding
wait

# Proceed with deployment regardless of the test results
echo "Proceeding with deployment regardless of test results."
python main.py  # Replace this with your actual deployment start-up command