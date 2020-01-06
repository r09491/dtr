#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "sepp.heid@t-online.de"
__doc__ = """ """

import argparse
import os
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

    rest_days = None

    first_day = date.today()
    logger.info("Today is the '{}' (as per computer).".format(first_day))

    try:
        input_day = date(*(int(input)
                           for input in args.last_working_day.split("-")))
    except ValueError:
        logger.error("Provide the last working day or birthday")
        return 1

    if args.free_days > args.free_days_per_year:
        logger.error("Free days exceed remaining days of year")
        return 2

    bavaria = Bavaria()

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

    """ """
    if years_todo == 0:  
        estimate_last_day = bavaria.sub_working_days(last_day, args.free_days)
        logger.info("The propable last working day is the '{}' ('{:d}' days free), a '{}'.".
                    format(estimate_last_day, args.free_days, estimate_last_day.strftime("%A")))
        logger.info("Is a working day: '{}'."
                    .format("yes" if bavaria.is_working_day(estimate_last_day)
                            else "no"))

    days_todo = bavaria.get_working_days_delta(first_day, last_day)
    logger.info("'{}' days and the rest of today to work in Bavaria."
                .format(days_todo))

    days_free = args.free_days
    if years_todo > 0:  
        """ The accumulated granted free working days before the last
        working yea r"""
        days_free += max(years_todo-1, 0)*args.free_days_per_year

        """ The granted free working day in the last year (Company
        regulation) """
        days_free += args.free_days_per_year \
            if last_day.month > 6 else args.free_days_per_year/2
        
    elif last_day.month < 7 and days_free > args.free_days_per_year/2: 
        """ Check the plausibility of the free working days in the
        last year (Company regulation) """
        logger.warning("'{}' exceed '{}'." .
                    format(days_free, args.free_days_per_year/2))

    days_todo -= days_free
    logger.info("'{}' working days without '{}' free days."
                .format(days_todo, days_free))
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
