# log_parser_tool

A simple CLI tool for parsing Apache/Nginx-style access logs and extracting basic information for quick analysis.

This tool is designed as a lightweight starting point for log investigation.  
In practice, log analysis often depends on the log format, the investigation purpose, and the type of suspicious activity you want to identify.  
Because of that, the parsing rules and output format are expected to be adjusted as needed.

## Features

- Count total requests
- Summarize requests by IP address
- Summarize HTTP status codes
- Summarize requested URL paths
- Extract bot-like User-Agents
- Extract 404 records
- Export summary results as CSV files with `--output-dir`

## Requirements

- Python 3.10+

## Usage

```bash
python log_parser.py sample_access.log.txt
python log_parser.py sample_access.log.txt --output-dir output
python log_parser.py --help
```


## Output files

When `--output-dir` is specified, the tool writes CSV files such as:

* `top_ips.csv`
* `status_codes.csv`
* `top_paths.csv`
* `bot_user_agents.csv`
* `errors_404.csv`

## Supported log format

Currently, this tool assumes an Apache combined log format-like structure.

If your log format is different, you may need to adjust the parsing rule in `LOG_PATTERN`.

## Design idea

This is not intended to be a complete or universal log analysis solution.
Instead, it is meant to serve as a simple and flexible base tool for investigating access logs and extracting the most basic operational information.

Typical things you may want to customize include:

* parsing rules for different log formats
* extraction targets for suspicious requests
* output fields and report style
* filtering conditions depending on the investigation purpose

## Example use cases

* Quick inspection of web access logs
* Checking top client IPs and frequently requested paths
* Reviewing 404 activity
* Identifying bot-like or script-based access
* Creating a small base tool for further operational investigation