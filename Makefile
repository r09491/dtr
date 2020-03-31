DTR=.


## to be executed under linux
.PHONY: dtr
dtr:
	$(DTR)/dtr.py --free_days_per_year 36 --hours_on_konto 40 "1954-12-10" 

.PHONY: clean
clean: 
	rm *~
