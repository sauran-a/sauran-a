# Report Monaco

A Python package that creates and prints report of Monaco 2018 Racing.

For using the package requires 3 files with data, with specific formatting. Files include:
* abbreviations.txt - contains racer's information. Ex:
`DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER`
* start.log - contains each racer's start time. Ex: `SVF2018-05-24_12:02:58.917`
* end.log - contains each racer's finish time. Ex: `SVF2018-05-24_12:04:51.219`

# Methods
* [`main`](#main)
* [`read_log(path)`](#read_log)
* [`build_report(abbr_path, startlog_path, endlog_path)`](#build_report)
* [`print_report()`](#print_report)
* [`cli_interface()`](#cli_interface)

## main

---
Prints Monaco 2018 Race results, with racer's place, name, team and best time sorted from the top to bottom
## read_log

---
Expects a path to a log file as an argument. Opens provided file and puts data into list of dicts, where each list object contains racer's name and their time

### Parameters

* :param file: path to a file containing racers abbreviations and their time

### Returns
A list of dicts, containing each racer's abbreviation and time

## build_report

---
Expects 3 paths to a files in following order: 
* abbreviations.txt
* start time log
* finish time log.

Calculates each racer's best time and creates new list of dicts containing racer's abbreviation and best time.
Then list is being sorted by racer's place. Finally, merges racers result with their personal information like
full name and club into one list.

### Parameters
* :param abbreviations_file_path: path to a file containing racers abbreviations and other personal information
* :param start_log: path to a file containing racers abbreviation and start time
* :param end_log: path to a file containing racers abbreviation and end time

### Returns
A list of dicts, containing each racer's abbr., full name, club  and best time in the race sorted from the best to the worst results.

## print_report

---
Expects a list of dicts, containing racers name, club and best time Prints each racer's information, according to his position in the race if given only racers_list.

If provided with "cli" mode prints racers in optional order (by default in ascending).

### Parameters
* :param racers_list: list of dicts containing racer's abbr., full name, club and best time
* :param mode: can be None or "cli" if used with command line interface

## cli_interface

---
Command-line interface to display race results.

Required arguments:

`--file` - path to files with racers abbreviation, start and end time log

Optional arguments:

`--asc`/`--desc` - print race results in either ascending or descending order

`--driver` - provided with racer full name prints only their result in the race