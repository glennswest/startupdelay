#!/bin/bash
start_time=$(date +"%Y-%m-%d %H:%M:%S.%3N")
echo "Test start time: $start_time"
prev_time=$(date +%s.%N)
while true; do
  # Wait for 0.5 seconds
  sleep 0.5
  # Record the current timestamp
  current_time=$(date +%s.%N)

  # Calculate the time difference (using awk)
  diff=$(echo "$current_time $prev_time" | awk '{print $1 - $2}')

  # Human-readable timestamp (with milliseconds)
  readable_time=$(date +"%Y-%m-%d %H:%M:%S.%3N")

  # Print current time and the difference from the previous time
  echo "Current time: $readable_time, Time difference from previous: $diff seconds"

  # Update the previous time
  prev_time=$current_time
done

