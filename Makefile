DTR=$(HOME)/1WORK/dtr


## to be executed under linux
.PHONY: sepp
sepp:
	@$(DTR)/dtr.py --free_days_per_year 40 --hours_on_konto 4 "1954-12-10"

.PHONY: roswitha
roswitha:
	@$(DTR)/dtr.py --free_days_per_year 0 --free_days_left 0 --hours_per_day 0 "1957-04-25"

.PHONY: sebi
sebi:
	@$(DTR)/dtr.py --free_days_per_year 30 --free_days_left 30 "1982-08-08"

.PHONY: josef
josef:
	@$(DTR)/dtr.py --free_days_per_year 30 --free_days_left 30 "1989-05-12"

.PHONY: clean
clean: 
	rm *~
