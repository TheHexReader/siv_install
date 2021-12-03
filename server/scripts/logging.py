import os
import datetime

class Log:
    SUCCSESS = 'SUCCSESS'
    FAIL = 'FAIL'
    WARNING = 'WARNING'

    def log(str, status):
        now = datetime.datetime.now()
        if os.path.isfile(f"./logs/{now.date()}.log"):
            open(f"./logs/{now.date()}.log", "a").write(f"\n[{now.time()}][STATUS-{status}] - {str}")
        else:
            open(f"./logs/{now.date()}.log", "w+").write(f"[{now.time()}][STATUS-{status}] - {str}")


if __name__ == "__main__":
    Log.log("Test of log!", Log.SUCCSESS)