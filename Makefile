DTR=.


## to be executed under linux
.PHONY: dtr
dtr:
	$(DTR)/dtr.py --free_days 9 --hours_on_konto 50 "1954-12-10" 

.PHONY: clean
clean: 
	rm *~
