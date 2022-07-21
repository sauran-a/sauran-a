import re
from datetime import datetime, timedelta
from collections import defaultdict
import argparse
import sys

# Constants to store path to files
ABBREVIATIONS = 'files/abbreviations.txt'
START_LOG = 'files/start.log'
END_LOG = 'files/end.log'


def main():
    """
    When opened without CLI arguments prints racer's place, name, team and best time sorted from the top to bottom
    """

    top = build_report(ABBREVIATIONS, START_LOG, END_LOG)
    print_report(top)


def read_log(file):
    """
    Opens provided file and puts data into list of dicts, where each list object contains racer's name and their time

    Parameters
    ----------
    :param file:
        path to a file containing racers abbreviations and their time

    Returns
    -------
    list of dicts
        The list of dicts, containing each racer's abbreviation and time
    """

    time_list = list()
    with open(file) as start_end_log:
        for line in start_end_log:
            match = re.match(r"(?P<name>[A-Za-z]+).*(?P<time>\d{2}:\d{2}:\d{2}.\d{3})", line)
            if match:
                date_time_obj = datetime.strptime(match.group("time"), "%H:%M:%S.%f")
                item = {"abr": match.group("name"), "time": date_time_obj}
                time_list.append(item)

    return time_list


def build_report(abbreviations_file_path, start_log, end_log):
    """
    Opens start.log, end.log and abbreviations.txt files and creates list of dicts for each of them.

    Calculates each racer's best time and creates new list of dicts containing racer's abbreviation and best time.
    Then list is being sorted by racer's place. Finally, merges racers result with their personal information like
    full name and club into one list.

    Parameters
    ----------
    :param abbreviations_file_path:
        path to a file containing racers abbreviations and other personal information
    :param start_log:
        path to a file containing racers abbreviation and start time
    :param end_log:
        path to a file containing racers abbreviation and end time

    Returns
    -------
    list of dicts
        The list of dicts, containing each racer's abbr., full name, club
        and best time in the race sorted from the best to the worst results.
    """

    # Get lists of dicts, containing racers with their start and end time
    start_time = read_log(start_log)
    end_time = read_log(end_log)

    # Calculate each racer's best time
    race_results = list()
    for i in range(len(start_time)):
        for k in range(len(end_time)):
            if start_time[i]["abr"] == end_time[k]["abr"]:
                duration = end_time[k]["time"] - start_time[i]["time"]
                if timedelta(seconds=1) > duration:
                    duration = start_time[i]["time"] - end_time[k]["time"]
                    best_time = {"abr": start_time[i]["abr"], "time": str(duration)}
                else:
                    best_time = {"abr": start_time[i]["abr"], "time": str(duration)}
                race_results.append(best_time)

    results_sorted = sorted(race_results, key=lambda x: x['time'])

    # Get a list of dicts, containing racers' personal information
    racers_info = list()
    with open(abbreviations_file_path) as abbr:
        for line in abbr:
            match = re.match("(?P<abr>.*)_(?P<full_name>.*)_(?P<club>.*)", line)
            if match:
                racer = {"abr": match.group("abr"), "full_name": match.group("full_name"), "club": match.group("club")}
                racers_info.append(racer)

    # Merge racers' best time with their personal information
    d = defaultdict(dict)
    for line in (results_sorted, racers_info):
        for elem in line:
            d[elem["abr"]].update(elem)

    return d.values()


def print_report(racers_list, mode=None):
    """
    Prints each racer's information, according to his position in the race if given only racers_list.

    If provided with "cli" mode prints racers in optional order (by default in ascending).

    Parameters
    ----------
    :param racers_list:
        list of dicts containing racer's abbr., full name, club and best time
    :param mode:
        can be None or "cli" if used with command line interface
    """

    # Print individual racer's result
    if mode == "cli":
        print(f"{racers_list['full_name']} | {racers_list['club']} | {racers_list['time']}")

    # Print all racers with their result
    elif mode is None:
        for count, value in enumerate(racers_list, start=1):
            if count == 16:
                print("---------------------------------------------------------")
            print(f"{count:>2}. {value['full_name']:<20} | {value['club']:<25} | {value['time']}")


def cli_interface():
    """
    Command-line interface to display race results.

    Required arguments:
    -- file - path to files with racers abbreviation, start and end time log

    Optional arguments
    --asc/--desc - print race results in either ascending or descending order
    --driver - provided with racer full name prints only their result in the race
    """

    parser = argparse.ArgumentParser(description="Shows list of drivers or statistic on specific driver "
                                                 "when given specific arguments. If no arguments are given"
                                                 "then prints top racers")
    parser.add_argument("--file", help="shows list of drivers from provided file "
                                       "and optional order (default order is asc)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--asc", action='store_const', const="asc", dest="sort")
    group.add_argument("--desc", action='store_const', const="desc", dest="sort")
    parser.set_defaults(sort="asc")
    parser.add_argument("--driver", help="Provide a string to count", type=str)
    args = parser.parse_args()

    abbr, start, end = args.file.split()
    race_results = build_report(abbr, start, end)

    if args.file and not args.driver:
        if args.sort == "asc":
            print_report(race_results)

        if args.sort == "desc":
            race_results = sorted(race_results, key=lambda y: y['time'], reverse=True)
            print_report(race_results)

    if args.file and args.driver:
        x = next((item for item in race_results if item["full_name"] == args.driver), None)
        print_report(x, mode="cli")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        cli_interface()
