#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "sepp.heid@t-online.de"
__doc__ = """ """

import argparse
import os
import os.path
import sys

from datetime import date
from datedelta import datedelta
from workalendar.europe import Bavaria

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(sys.argv[0]))

__version__ = "0.0.0"
__author__ = "sepp.heid@t-online.de"

LIFE_EXPECTATION = 80.4


def to_date(of_date_string):
    return date(*(int(part) for part in of_date_string.split("-")))


def free_days_from(from_day, of_free_days, working_days_delta):
    home = os.path.expanduser('~')
    vacationfile = os.path.join(home, '.dtr')

    try:
        with open(vacationfile, 'r') as dtr:
            vacations = sorted(dtr.read().strip().split('\n'))
    except:
        return of_free_days
                         
    vacations = [v.split() for v in vacations
                 if not v.startswith('#')]
    vacations = [(to_date(start), to_date(stop))
                 for start, stop in vacations]
    vacations = [(start, stop) for start, stop in vacations
                 if stop >= start and stop >= from_day]
    free_days = sum([working_days_delta(stop, start) + 1
                     for start, stop in vacations])

    first_slot = vacations[0]
    first_slot_start = first_slot[0]
    first_slot_days = working_days_delta(from_day, first_slot_start) \
                      if first_slot_start < from_day else 0

    return free_days - first_slot_days 


def taken_days_until(until_day, working_days_delta):
    home = os.path.expanduser('~')
    vacationfile = os.path.join(home, '.dtr')

    try:
        with open(vacationfile, 'r') as dtr:
            vacations = sorted(dtr.read().strip().split('\n'))
    except:
        return 0
                         
    vacations = [v.split() for v in vacations
                 if not v.startswith('#')]
    vacations = [(to_date(start), to_date(stop))
                 for start, stop in vacations]
    vacations = [(start, stop) for start, stop in vacations
                 if stop < until_day]
    taken_days = sum([working_days_delta(stop, start) + 1
                      for start, stop in vacations])

    return taken_days


def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description="Calculates the day to retirement in Bavaria",
        epilog="Provide the retirement day or birthday")

    parser.add_argument("--version", action="version", version=__version__)

    parser.add_argument("--free_days", type=int, default=0,
                        help="The free days left in the current year")

    parser.add_argument("--free_days_per_year", type=int, default=30,
                        help="The granted maximum free days in a year")

    parser.add_argument("--hours_per_day", type=int, default=8,
                        help="The required working hours per day")

    parser.add_argument("--hours_on_konto", type=int, default=0,
                        help="The hours worked in advance")

    parser.add_argument("last_working_day",
                        help="The date of the last working day or birthday")

    return parser.parse_args()


def main():
    args = parse_arguments()

    bavaria = Bavaria()

    rest_days = None

    first_day = date.today()
    logger.info("Today is the '{}' (as per computer).".format(first_day))

    try:
        input_day = to_date(args.last_working_day)
    except ValueError:
        logger.error("Provide the last working day or birthday")
        return 1

    if args.free_days > 0:
        logger.info("Using free days from command line.")
        free_days = args.free_days
    else:
        logger.info("Using planing from vacation file.")
        free_days = free_days_from( first_day,
                                    args.free_days_per_year,
                                    bavaria.get_working_days_delta)        

    plan_days_left = args.free_days_per_year - free_days 
    logger.info("Planning with '{:d}' free days, '{:d}' days still left."
                .format(free_days, plan_days_left))


    if free_days > args.free_days_per_year:
        logger.error("Free days exceed official remaining days of year")
        return 2

    if input_day < first_day:
        logger.info("Day of birth is the '{}' (as per input), a '{}'".
                    format(input_day, input_day.strftime("%A")))

        life_expect = divmod(LIFE_EXPECTATION, 1)
        death_day = input_day + datedelta(years=int(life_expect[0]),
                                          months=int(life_expect[1]*12))
        logger.info("Day of death is after the '{}' (propability 66.7%), a '{}'."
                    .format(death_day, death_day.strftime("%A")))

        life_days = (first_day-input_day).days
        logger.info("'{}' days alive! Congratulations!".format(life_days))

        rest_days, total_days = (death_day-first_day).days, \
            (death_day-input_day).days
        logger.info("At least another '{}' out of '{}' days to live ({:.1f}%)."
                    .format(rest_days, total_days,
                            100.0*(rest_days/total_days)))

        birthday_65 = input_day + datedelta(years=65)
        logger.info("The 65th birthday is the '{}', a '{}'.".
                    format(birthday_65, birthday_65.strftime("%A")))
        logger.info("Is a working day: '{}'."
                    .format("yes" if bavaria.is_working_day(birthday_65)
                            else "no"))

        months_65 = min(birthday_65.year - 2011, 24)
        logger.info("Additional '{}' months to work in Germany."
                    .format(months_65))

        last_day = birthday_65 + datedelta(months=months_65+1)
        last_day = date(last_day.year, last_day.month, 1) - datedelta(days=1)
        logger.info("The official last day before retirement is the '{}', a '{}'."
                    .format(last_day, last_day.strftime("%A")))
        logger.info("Is a working day: '{}'."
                    .format("yes" if bavaria.is_working_day(last_day)
                            else "no"))

        """ Check the plausibility of the free working days in the last year"""

    else:
        logger.info("The input day '{}' is considered the last working day.".
                    format(input_day))
        last_day = input_day

        
    years_todo = last_day.year - first_day.year
    if years_todo == 0:
        earliest_last_day = bavaria.sub_working_days(last_day, args.free_days_per_year)
        logger.info("The earliest last working day is the '{}' ('{:d}' days max free), a '{}'.".
                    format(earliest_last_day, args.free_days_per_year, earliest_last_day.strftime("%A")))

        taken_days = taken_days_until(earliest_last_day, bavaria.get_working_days_delta)        
        logger.info("'{:d}' free days are spent until earliest last day.".format(taken_days))
        free_days_left = free_days - taken_days
        logger.info("'{:d}' planned days are left at the earliest last day.".format(free_days_left))
        estimate_last_day = bavaria.add_working_days(earliest_last_day, taken_days)
        logger.info("The propable last working day is the '{}', a '{}'.".
                    format(estimate_last_day, estimate_last_day.strftime("%A")))
        logger.info("Is a working day: '{}'."
                    .format("yes" if bavaria.is_working_day(estimate_last_day)
                            else "no"))

        
    days_todo = bavaria.get_working_days_delta(first_day, last_day)
    logger.info("'{}' days and the rest of today to work in Bavaria."
                .format(days_todo))

    if years_todo > 0:  
        """ The accumulated granted free working days before the last
        working year """
        free_days += max(years_todo-1, 0)*args.free_days_per_year

        """ The granted free working day in the last year (Company
        regulation) """
        free_days += args.free_days_per_year \
            if last_day.month > 6 else args.free_days_per_year/2
        
    elif last_day.month < 7 and free_days > args.free_days_per_year/2: 
        """ Check the plausibility of the free working days in the
        last year (Company regulation) """
        logger.warning("'{}' exceed '{}'." .
                    format(free_days, args.free_days_per_year/2))

    days_todo -= free_days
    days_todo -= plan_days_left
    logger.info("'{}' working days without '{}' free days and '{}' left days."
                .format(days_todo, free_days, plan_days_left))
    if rest_days is not None:
        logger.info("'{:.1f}%' of remaining life span still to work."
                    .format(100.0*(days_todo/rest_days)))

        

    logger.info("'{}' working hours left without konto hours."
                .format(args.hours_per_day*days_todo))
    if args.hours_on_konto != 0:
        logger.info("'{}' working hours left with '{}' konto hours."
                    .format(args.hours_per_day*days_todo - args.hours_on_konto,
                            args.hours_on_konto))

    return 0


if __name__ == "__main__":
    sys.exit(main())
