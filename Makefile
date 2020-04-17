DTR=$(HOME)/1WORK/dtr


## to be executed under linux
.PHONY: sepp
sepp:
	@$(DTR)/dtr.py --free_days_per_year 41 --hours_on_konto 4 "1954-12-10"

.PHONY: roswitha
roswitha:
	@$(DTR)/dtr.py --free_days_per_year 0 --free_days 0 --hours_per_day 0 "1957-04-25"

.PHONY: clean
clean: 
	rm *~
