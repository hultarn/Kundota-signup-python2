import requests
import json
from tabulate import tabulate
from datetime import timedelta
import datetime

class BollSvenskan:
    BASE = "https://nextcloud.jacobadlers.com/index.php"
    tokenPairs = {}

    def __init__(self, name=None):
        self.name = name
        self.session = requests.session()

        self.headers = self.getHeaders()
        self.currentPoll = json.loads(self.session.get("https://api.bollsvenskan.jacobadlers.com/dota/signup").text)['currentPollUrl'].split('/')[-1]
        self.currentGameIDS = self.getCurrentGameIDS()

    def getCSRFToken(self):       
        csrf_token = self.session.get(BollSvenskan.BASE + "/csrftoken")
        res = json.loads(csrf_token.text)

        return res['token']

    def getHeaders(self):
        return {
        'origin': 'https://nextcloud.jacobadlers.com',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        'requesttoken': self.getCSRFToken()
        }

    def getCurrentGameIDS(self):
        get_list_req = self.session.get(f"https://nextcloud.jacobadlers.com/index.php/apps/polls/s/{self.currentPoll}/options", headers=self.headers)
        res = json.loads(get_list_req.text)
        
        return [i['id'] for i in res['options']]

    def sign(self, gameID, bool) -> bool:
        def checkUsername():
            check_name_payload = {
                'token': self.currentPoll,
                'userName': self.name
            }

            check_name_req = self.session.post(BollSvenskan.BASE + "/apps/polls/check/username", headers=self.headers, data=check_name_payload)
            if not check_name_req.ok:
                print("Failed namecheck", check_name_req)
                return False
            return True
        
        def register():
                register_payload = {
                    'userName': self.name,
                    "emailAddress": ""
                }

                register_req = self.session.post(BollSvenskan.BASE + f"/apps/polls/s/{self.currentPoll}/register", headers=self.headers, data=register_payload)
                if not register_req.ok:
                    print("Failed register", register_req)
                    return False

                res = json.loads(register_req.text)
                token = res['share']['token']

                BollSvenskan.tokenPairs[self.name] = token

                print(BollSvenskan.tokenPairs[self.name])

                return True

        def signGame() -> bool:
            VOTE = f"/apps/polls/s/{BollSvenskan.tokenPairs[self.name]}/vote"

            vote_payload = {
                "optionId": self.currentGameIDS[gameID],
                "setTo": "yes" if bool else "no"
            }

            print("1", BollSvenskan.tokenPairs)

            vote_req = self.session.put(BollSvenskan.BASE + VOTE, headers=self.headers, data=vote_payload)
            print(vote_req.ok)

            if not vote_req.ok:
                return False

            print(f"signed up/down {self.name} for game {self.currentGameIDS[gameID]}")

            return True

        if not self.name in BollSvenskan.tokenPairs:
            if not checkUsername():
                print("Failed checkUsername")
                return False
            if not register():
                print("Failed register")
                return False
        if not signGame():
            print("Failed signGame")
            return False

        return True

    def getList(self) -> str:
        def refactorThis(res):
            a = {"19:30": [], "20:45": [], "22:0": []}
            names = []

            d = datetime.datetime.today().replace(microsecond=0)
            t = datetime.timedelta((13 - d.weekday()) % 7)
            c = d + t
            c = c.replace(hour=0)

            for i in res["votes"]:
                t = datetime.datetime.strptime(i["optionText"], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None) + timedelta(hours=1)
                if not t < c:
                    t2 = str(t.hour) + ":" + str(t.minute)
                    a[t2].append(["[0;34m" + i["user"]["displayName"], i["answer"]])
                    names.append("[0;34m" + i["user"]["displayName"])
                    
            a["19:30"] ={ i[0] : i[1] for i in sorted(a["19:30"]) }
            a["20:45"] = { i[0] : i[1] for i in sorted(a["20:45"]) }
            a["22:0"] = { i[0] : i[1] for i in sorted(a["22:0"]) }
            names = sorted(list(dict.fromkeys(names)))

            t = []
            count = ["[0;34mTotal", 0,0,0]
            for n in names:
                if n in a["19:30"] and a["19:30"][n] == "yes":
                    count[1] += 1
                if n in a["20:45"] and a["20:45"][n] == "yes":
                    count[2] += 1
                if n in a["22:0"] and a["22:0"][n] == "yes":
                    count[3] += 1

                t.append([n, 
                        "[0;32mYes" if n in a["19:30"] and a["19:30"][n] == "yes" else "[0;31mNo", 
                        "[0;32mYes" if n in a["20:45"] and a["20:45"][n] == "yes" else "[0;31mNo", 
                        "[0;32mYes" if n in a["22:0"] and a["22:0"][n] == "yes" else "[0;31mNo"])

            for i in range(len(count)):
                count[i] = str(count[i])

            t.append(count)

            ret = tabulate(t, headers=['[0;34mTime','[0;34m19:30', '[0;34m20:45', '[0;34m22:00'])

            return ret.replace("Total", ret.split("\n")[1] + "\n" + "Total")
        
        get_list_req = self.session.get(f"https://nextcloud.jacobadlers.com/index.php/apps/polls/s/{self.currentPoll}/votes", headers=self.headers)
        res = json.loads(get_list_req.text)

        return refactorThis(res)




   