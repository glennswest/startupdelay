# Startup Delay Testing Suite

This testing suite is designed to measure and monitor system responsiveness and startup delays on OpenShift cluster nodes, particularly master nodes. It works with both cgroup v1 and cgroup v2 environments.

## Purpose

The test suite measures system scheduling delays by running a continuous loop with 0.5-second sleep intervals and tracking the actual time differences between iterations. Delays beyond the expected 0.5 seconds indicate system responsiveness issues, which can help identify:

- Process scheduling delays
- System resource contention  
- Container runtime performance issues
- Node-level performance degradation

## Files Overview

| File | Purpose |
|------|---------|
| `runtest.sh` | Main test launcher - starts the test in background |
| `test.sh` | Core test script that measures timing intervals |
| `watchit.sh` | Monitoring wrapper using `watch` command |
| `watch.py` | Python script that analyzes results and tracks min/max values |
| `minmax.json` | Historical record of minimum and maximum delay changes |

## Quick Start

### Running the Test

```bash
# Start the startup delay test
./runtest.sh
```

This will:
- Run the test in the background
- Generate output in `test.log`
- Continue running until manually stopped

### Monitoring Results

```bash
# Watch real-time analysis of results
./watchit.sh
```

This will display:
- Current minimum and maximum delay times
- Line count of processed entries
- Alerts when new min/max records are detected

### Stopping the Test

```bash
# Find and stop the test process
pkill -f "test.sh"
# or
ps aux | grep test.sh
kill <PID>
```

## Detailed Component Description

### runtest.sh
Simple launcher script that:
- Starts `test.sh` in the background
- Redirects output to `test.log`
- Allows the test to run independently

### test.sh
Core measurement script that:
- Records precise timestamps using `date +%s.%N` (nanosecond precision)
- Sleeps for 0.5 seconds each iteration
- Calculates actual time differences between iterations
- Outputs human-readable timestamps and timing data
- Runs in an infinite loop until terminated

**Expected behavior**: Time differences should be approximately 0.500-0.505 seconds under normal conditions.

### watchit.sh
Monitoring wrapper that:
- Uses the `watch` command to run `watch.py` repeatedly
- Provides real-time updates of the analysis
- Refreshes the display automatically

### watch.py
Analysis and tracking script that:
- Parses `test.log` for timing measurements
- Maintains running minimum and maximum delay values
- Detects when new records are set
- Writes historical data to `minmax.json`
- Maintains current state in `.maxmin` file
- Provides console output when min/max values change

**Key features**:
- Initializes with min=100.0, max=-100.0 for first-run detection
- Tracks line numbers for easy log correlation
- Preserves full log lines where records were set
- Handles decimal parsing and validation

## Output Format

### Console Output (from watch.py)
```
Min Value Line: Current time: 2025-08-25 13:29:53.173, Time difference from previous: 0.502227 seconds
Max Value Line: Current time: 2025-08-25 13:31:52.415, Time difference from previous: 0.516031 seconds  
Min = 0.502227 Max = 0.516031 Lines = 238
```

### minmax.json Format
```json
{
    "min": 0.502227,
    "max": 0.516031,
    "line": "Current time: 2025-08-25 13:31:52.415, Time difference from previous: 0.516031 seconds\n",
    "lineno": 238
}
```

Each entry records:
- `min`: Current minimum delay observed
- `max`: Current maximum delay observed  
- `line`: The exact log line where this min/max was recorded
- `lineno`: Line number in the log file

## Interpreting Results

### Normal Behavior
- **Expected range**: 0.500-0.510 seconds
- **Baseline minimum**: ~0.500-0.502 seconds
- **Acceptable maximum**: <0.520 seconds

### Warning Signs
- **High maximum delays**: >0.600 seconds indicate system stress
- **Increasing trend**: Growing maximum values over time
- **Wide variance**: Large gaps between min/max suggest inconsistent performance

### Critical Issues  
- **Extreme delays**: >1.0 second indicates severe system issues
- **Frequent spikes**: Regular high delays suggest resource contention
- **Baseline shift**: Minimum values increasing over time

## Platform Compatibility

### OpenShift Environments
- **Master nodes**: Preferred deployment location
- **Worker nodes**: Also supported but may show different patterns
- **cgroup v1**: Fully supported
- **cgroup v2**: Fully supported

### System Requirements
- Bash shell
- Python 3.x
- Standard Unix utilities (`date`, `sleep`, `watch`)
- Write permissions in the current directory

## Troubleshooting

### Common Issues

**Test not starting**:
```bash
# Check if script is executable
chmod +x runtest.sh test.sh watchit.sh

# Verify dependencies
which python3
which watch
```

**No output in monitoring**:
```bash
# Check if test.log exists and is being written
ls -la test.log
tail -f test.log
```

**Python script errors**:
```bash
# Run analysis manually to see errors
python3 watch.py
```

### Log File Management

The test generates continuous output. For long-running tests, consider:

```bash
# Rotate logs periodically
mv test.log test.log.$(date +%Y%m%d_%H%M%S)
# Test will create a new test.log automatically
```

### Performance Impact

This test suite has minimal system impact:
- Single background process
- 0.5-second sleep intervals
- Lightweight Python analysis
- Small log file generation rate (~2 entries/second)

## Use Cases

### Performance Monitoring
- Continuous monitoring of node responsiveness
- Baseline establishment for cluster nodes
- Performance regression detection

### Troubleshooting
- Identifying intermittent scheduling issues
- Correlating delays with system events
- Validating performance optimizations

### Capacity Planning
- Understanding node performance characteristics
- Measuring impact of workload changes
- Establishing SLA baselines

## Data Retention

- `test.log`: Grows continuously, rotate as needed
- `minmax.json`: Append-only historical record
- `.maxmin`: Current state file, can be deleted to reset tracking

## Integration

This suite can be integrated with monitoring systems by:
- Parsing `minmax.json` for metrics collection
- Monitoring log growth rates
- Alerting on delay thresholds
- Correlating with other system metrics 