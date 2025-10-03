from script import mainQ, update_ip
import time

def run_loop():
    update_ip()
    timesRan = 0
    while True:
        mainQ()
        time.sleep(2)
        timesRan += 1
        print("TIMESRAN:" + str(timesRan))

if __name__ == "__main__":
    run_loop()
