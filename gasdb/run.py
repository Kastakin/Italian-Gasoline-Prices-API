from db_updater import db_updater, table_creator
import schedule
import time

creator = table_creator
updater = db_updater


if __name__ == "__main__":
    creator()
    updater()
    schedule.every().day.at("09:00").do(updater)
    

    while True:
        schedule.run_pending()
        time.sleep(1) # wait one second
