DTR=.


## to be executed under linux
.PHONY: dtr
dtr:
	$(DTR)/dtr.py --free_days 30 --hours_on_konto 28 "1954-12-10" 

.PHONY: clean
clean: 
	rm *~
