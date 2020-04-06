DTR=$(HOME)/1WORK/dtr


## to be executed under linux
.PHONY: dtr
dtr:
	$(DTR)/dtr.py --free_days_per_year 41 --hours_on_konto 4 "1954-12-10" 

.PHONY: clean
clean: 
	rm *~
