from data_service import DataService
from sms_service import SMSService
from datetime import datetime
from time import sleep

def main():
    dataService = DataService()
    smsService = SMSService()
    morning_update_given = False
    night_update_given = False
    prevDate = None
    while True:
        dataService.fetch_todays_games()

        newDate = datetime.today()
        if prevDate != newDate:
            morning_update_given = False
        prevDate = newDate

        # Send the list of all games in the morning around 9 AM
        if not morning_update_given and newDate.hour > 9 and newDate.hour < 10:
            if len(dataService.todays_games) > 0:
                smsService.send_message(dataService.build_morning_message())
            morning_update_given = True
            night_update_given = False

        # Send the final scores and stat leaders of each game when all games are Final
        if not night_update_given and (game["status"] == "Final" for game in dataService.todays_games):
            if (len(dataService.todays_games) > 0):
                smsService.send_message(dataService.build_night_message())
            night_update_given = True

        sleep(10 * 60)



if __name__ == "__main__":
    main()

    
    