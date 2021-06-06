import requests
sender=input("what is ur name")
bot_message=""
while bot_message != "Bye":
    message = input("what's your message?\n")
    print("sending message now...")
    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"sender": sender, "message": message})
    print("bot says, ",end='')
    for i in r.json():
        bot_message = i['text']
        print(f"{i['text']}")