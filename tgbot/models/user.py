class User:
    def __init__(self, user_id, notifications_enabled=True):
        self.user_id = user_id
        self.notifications_enabled = notifications_enabled
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'notifications_enabled': self.notifications_enabled
        }