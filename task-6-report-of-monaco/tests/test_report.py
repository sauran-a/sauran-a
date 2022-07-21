import argparse
from unittest import mock
from unittest.mock import patch
import datetime
from src.report_monaco import report


@patch('builtins.open', mock.mock_open(read_data='SVF2018-05-24_12:02:58.917'))
def test_read_log():
    assert report.read_log('random_string') == [
        {'abr': 'SVF', 'time': datetime.datetime(1900, 1, 1, 12, 2, 58, 917000)}]


def test_print_report_default(capsys):
    racers_list = [
        {'abr': 'SVF', 'time': '0:01:04.415000', 'full_name': 'Sebastian Vettel', 'club': 'FERRARI'},
        {'abr': 'VBM', 'time': '0:01:12.434000', 'full_name': 'Valtteri Bottas', 'club': 'MERCEDES'}
    ]
    report.print_report(racers_list)
    captured = capsys.readouterr()
    assert captured.out == ' 1. Sebastian Vettel     | FERRARI                   | 0:01:04.415000\n' \
                           ' 2. Valtteri Bottas      | MERCEDES                  | 0:01:12.434000\n'


def test_print_report_driver(capsys):
    racer = {'abr': 'SVF', 'time': '0:01:04.415000', 'full_name': 'Sebastian Vettel', 'club': 'FERRARI'}
    report.print_report(racer, mode="cli")
    captured = capsys.readouterr()
    assert captured.out == 'Sebastian Vettel | FERRARI | 0:01:04.415000\n'


def test_build_report():
    results = list(report.build_report('files/abbreviations_test.txt', 'files/start_test.log', 'files/end_test.log'))
    comparing_list = [
        {'abr': 'SVF', 'time': '0:01:04.415000', 'full_name': 'Sebastian Vettel', 'club': 'FERRARI'},
        {'abr': 'DRR', 'time': '0:02:47.987000', 'full_name': 'Daniel Ricciardo', 'club': 'RED BULL RACING TAG HEUER'}
    ]
    assert results == comparing_list


@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(file='files/abbreviations_test.txt files/start_test.log files/end_test.log',
                                       sort='asc',
                                       driver=None))
def test_cli_no_driver_asc(mock_args, capsys):
    report.cli_interface()
    captured = capsys.readouterr()
    assert captured.out == ' 1. Sebastian Vettel     | FERRARI                   | 0:01:04.415000\n' \
                           ' 2. Daniel Ricciardo     | RED BULL RACING TAG HEUER | 0:02:47.987000\n'


@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(file='files/abbreviations_test.txt files/start_test.log files/end_test.log',
                                       sort='desc',
                                       driver=None))
def test_cli_no_driver_desc(mock_args, capsys):
    report.cli_interface()
    captured = capsys.readouterr()
    assert captured.out == ' 1. Daniel Ricciardo     | RED BULL RACING TAG HEUER | 0:02:47.987000\n' \
                           ' 2. Sebastian Vettel     | FERRARI                   | 0:01:04.415000\n'


@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(file='files/abbreviations_test.txt files/start_test.log files/end_test.log',
                                       driver='Daniel Ricciardo'))
def test_cli_interface_with_driver(mock_args, capsys):
    report.cli_interface()
    captured = capsys.readouterr()
    assert captured.out == 'Daniel Ricciardo | RED BULL RACING TAG HEUER | 0:02:47.987000\n'
