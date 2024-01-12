from generators.player_localizations import PLayerLocalization

class Player:

    def __init__(self):
        self.result = {}
        self.reset()

    def set_status(self,status = "ACTIVE"):
        self.result['account_status'] = status
        return self #возвращаем self здесь и ниже чтоб можно было одним за одним вызывать методы

    def sel_balance(self,balance = 0):
        self.result["balance"] = balance
        return self

    def set_avatar(self,avatar = "https://google.com/"):
        self.result["avatar"] = avatar
        return self

    def reset(self):
        self.sel_balance()
        self.set_avatar()
        self.set_status()
        self.result["localize"] = {
            "en": PLayerLocalization("en_US").build(),
            "ru": PLayerLocalization("ru_RU").build()
        }
        return self
    def update_inner_generator(self,key,generator):
        self.result[key] = {"en": generator.build()}
        return self
    def build(self):
        return self.result



'Example usage:'
# z = Player().build()
# print(z) #{'balance': 0, 'avatar': 'https://google.com/', 'account_status': 'ACTIVE', 'localize': {'en': {'nickname': 'Bryan'}, 'ru': {'nickname': 'Устин'}}}
# full = Player().sel_balance(100).set_status("BAD").set_avatar("chert").build()
# print(full) #{'balance': 100, 'avatar': 'chert', 'account_status': 'BAD', 'localize': {'en': {'nickname': 'Stephanie'}, 'ru': {'nickname': 'Самуил'}}}