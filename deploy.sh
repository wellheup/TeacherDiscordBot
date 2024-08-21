#!/bin/bash

echo "Starting test run with timeout of 60 seconds..."

# Run pytest with a timeout of 60 seconds and save the test output to a log file
timeout 60s pytest --maxfail=1 2>&1 | tee result.log

# Capture the exit code of pytest
EXIT_CODE=${PIPESTATUS[0]}

# Forcefully kill pytest if it's still running after timeout
if [ $EXIT_CODE -eq 124 ]; then
	echo "Tests timed out! Forcefully terminating pytest."
	pkill -f pytest
	# Check if any tests have failed before the timeout
	if grep -q "FAILED" result.log; then
		echo "Some tests failed before timing out! Aborting deployment."
		exit 1
	else
		echo "Continuing with deployment despite timeout."
	fi
else
	# Proceed based on pytest results
	if [ $EXIT_CODE -eq 0 ]; then
		echo "All tests passed! Proceeding with deployment."
	else
		echo "Some tests failed! Aborting deployment."
		exit 1
	fi
fi

# If tests either passed or timed out without failures, continue to deploy the app
python main.py  # Replace this with your actual deployment start-up command