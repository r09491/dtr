# dtr (days to retirement)
Calculates the  number of working days left from today to a day in the future considered the last working day subtracting all holidays in Bavaria. If it is in the past the specified day is considered a birthday and the day of retirement is automatically calculated as per German rules.


## Installation

1. Clone dtr

   $ git clone https://github.com/r09491/dtr.git

2. Enter the cloned directory

   $ cd dtr

3. Install the python3 virtualenv with python3 in the clone

   $ virtualenv -p python3 .vdtr

   You may want to add .vdtr to .gitignore

4. Activate the python3 virtualenv

   $ . .vdtr/bin/activate

5. Install the required python libraries

   $ pip install -r requirements.txt

## Example

```
(.vwork) @book:~/Work/dtr$ ./dtr.py --off 60 "1954-12-10"
INFO:dtr.py:Today is the '2019-06-05'.
INFO:dtr.py:Input day is the '1954-12-10'.
INFO:dtr.py:The input day is considered a birthday.
INFO:dtr.py:'23553' days alive today!
INFO:dtr.py:Current life expectation in Bavaria is about '80.4' years.
INFO:dtr.py:'2035-04-10' is the statistical last day of live.
INFO:dtr.py:Is a working day: yes.
INFO:dtr.py:Another '5788' out of '29341' days to live (19.7%).
INFO:dtr.py:The 65th birthday is on '2019-12-10'.
INFO:dtr.py:Is a working day: yes.
INFO:dtr.py:Another '8' months until retirement in Germany.
INFO:dtr.py:'2020-08-31' is the last day before retirement.
INFO:dtr.py:Is a working day: yes.
INFO:dtr.py:'308' days and the rest of today to spend with work in Bavaria.
INFO:dtr.py:'248' working days after subtracting '60' days vacation.
INFO:dtr.py:'4.3%' of remaining life still to work.
(.vwork) @book:~/Work/dtr$ 
```
