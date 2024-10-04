#!/bin/bash

echo "Running formatting for all files..."
run format_all.sh

echo "Starting test run with a timeout of 60 seconds..."

# Run pytest with a timeout and redirect output to a log file for future reference
> result_pytest.log
echo "Test started at: $(date)" >> result_pytest.log
timeout 60s pytest --maxfail=1 2>&1 | tee result_pytest.log

# Capture the exit code of pytest for debugging purposes
EXIT_CODE=${PIPESTATUS[0]}
echo "Exit code of pytest: $EXIT_CODE"

# Wait for pytest to finish running before proceeding
wait

# Proceed with deployment regardless of the test results
echo "Proceeding with deployment regardless of test results."

# Run the Flask application
echo "Starting Flask application..."
python3 main.py &

# Wait briefly to ensure Flask is up and running
sleep 5

# Run Cypress tests and log the output
# echo "Starting Cypress tests..."
# > result_cypress.log
# echo "Cypress tests started at: $(date)" >> result_cypress.log
# npx cypress run 2>&1 | tee result_cypress.log
# echo "Cypress tests completed."
