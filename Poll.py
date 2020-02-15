import matplotlib.pyplot as plt


class Poll:
    """

    """

    def __init__(self, lst, title, active=True):
        self.title = title
        self.cat_dict = {i: 0 for i in lst}
        self._voted = {}
        self.active = active

    def show_votes(self):
        print(self.cat_dict)

    def add_vote(self, s):
        if s in self.cat_dict:
            self.cat_dict[s] += 1
            print(f'added a vote to {s}')

    def exists(self, s):
        if s.lower() in self.cat_dict.keys():
            return True
        else:
            return False

    def poll_results(self):
        return self.cat_dict.items()

    def user_voted(self, user_id):
        self._voted[user_id] = 'voted'

    def did_vote(self, user_id):
        if user_id in self._voted:
            return True
        else:
            return False

    def set_active(self, active=True):
        self.active = active

    def get_active(self):
        return self.active

    def pie_votes(self):
        print('[INFO] making pie chart')
        labels = self.cat_dict.keys()
        values = self.cat_dict.values()
        plt.pie(values, labels=labels)
        plt.savefig('poll.png')