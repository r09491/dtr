DTR=.


## to be executed under linux
.PHONY: dtr
dtr:
	$(DTR)/dtr.py --free 48 "1954-12-10" 

.PHONY: clean
clean: 
	rm *~
