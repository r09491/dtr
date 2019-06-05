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
        prog = os.path.basename(sys.argv[0]),
        description = "Calculates the day to retirement in Bavaria",
        epilog = "Provide the retirement day or birthday")
    
    parser.add_argument("--version", action = "version", version=__version__)

    parser.add_argument("--off", type=int, default=0)
    
    parser.add_argument("last_working_day", nargs="*", 
                        help="The year, month, and day of the last working day or birthday")
    
    return parser.parse_args()



def main():
    args = parse_arguments()

    rest_days = None
    
    first_day = date.today()
    logger.info("Today is the '{}'.".format(first_day))

    try:
        input_day = date(*(int(input) for input in args.last_working_day))
    except:
        logger.error("Must provide the year, month and day of the last working day or birthday")
        return 1

    logger.info("Input day is the '{}'.".format(input_day))
    bavaria = Bavaria()
    
    if input_day < first_day:
        logger.info("The input day is considered a birthday.")
        logger.info("'{}' days alive today!".format((first_day-input_day).days))

        expect = divmod(LIFE_EXPECTATION,1)
        death_day = input_day + datedelta(years=int(expect[0]), months=int(expect[1]*12))
        logger.info("Current life expectation in Bavaria is about '{}' years."
                    .format(LIFE_EXPECTATION))
        logger.info("'{}' is the statistical last day of live.".format(death_day))
        logger.info("Is a working day: {}."
                    .format("yes" if bavaria.is_working_day(death_day) else "no"))

        rest_days, total_days = (death_day-first_day).days, (death_day-input_day).days
        logger.info("Another '{}' out of '{}' days to live ({:.1f}%)."
                    .format(rest_days, total_days, 100.0*(rest_days/total_days)))

        birthday_65 = input_day + datedelta(years=65)
        logger.info("The 65th birthday is on '{}'.".format(birthday_65))
        logger.info("Is a working day: {}."
                    .format("yes" if bavaria.is_working_day(birthday_65) else "no"))


        months_65 =  min(birthday_65.year - 2011, 24)
        logger.info("Another '{}' months until retirement in Germany.".format(months_65))

        last_day = birthday_65 + datedelta(months=months_65+1)
        last_day = date(last_day.year, last_day.month, 1) - datedelta(days=1)
        logger.info("'{}' is the last day before retirement.".format(last_day))
        logger.info("Is a working day: {}."
                    .format("yes" if bavaria.is_working_day(last_day) else "no"))

    else:
        logger.info("The input day is considered the last working day.")
        last_day = input_day
        
    days_todo = bavaria.get_working_days_delta(first_day, last_day)
    logger.info("'{}' days and the rest of today to spend with work in Bavaria."
                .format(days_todo))
    days_todo -= args.off
    logger.info("'{}' working days after subtracting '{}' days vacation."
                .format(days_todo, args.off))

    if rest_days is not None:
        logger.info("'{:.1f}%' of remaining life still to work."
                .format(100.0*(days_todo/rest_days)))
        
    return 0

        
if __name__ == "__main__":
    sys.exit(main())

