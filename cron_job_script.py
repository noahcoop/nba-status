from data_service import DataService
from sms_service import SMSService
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid arguments provided")
        exit(1)

    msgType = sys.argv[1]
    dataService = DataService()
    smsService = SMSService()
    dataService.fetch_todays_games()
    msg = ""
    
    if len(dataService.todays_games) > 0:
        if msgType == "morning":
            msg = dataService.build_morning_message()
        elif msgType == "night":
            msg = dataService.build_night_message()
    
    if msg != "":
        smsService.send_message(msg)
        print("Sent the following message to Noah's Phone:\n{}".format(msg))
    else:
        print("No message sent")