class User:
    telegram_id: int

    def __init__(self, telegram_id):
        self.telegram_id = telegram_id

    def get_user(self):
        return self.telegram_id
