"""Interface to the online high-score system"""

import json
import urllib
from serge.blocks import concurrent
import concurrent.futures


class OnlineMethodCallFailed(Exception):
    """Calling the online method resulted in an error"""


class OnlineScoreTable(object):
    """Simple interface to the online high score table"""

    def __init__(self, app_url, game):
        """Initialise the table connection"""
        self.app_url = app_url
        self.game = game

    def _getResult(self, method_url, parameters):
        """Returns the result of calling the web method url with the given parameters"""
        params = urllib.urlencode(list(parameters.iteritems()))
        url = '%s/%s?%s' % (self.app_url, method_url, params)
        url_file = urllib.urlopen(url)
        result = url_file.read()
        try:
            return json.loads(result)
        except ValueError, err:
            raise OnlineMethodCallFailed('JSON result invalid (%s). URL "%s" returned "%s"' % (err, url, result))

    def recordScore(self, player, category, score):
        """Record a score"""
        result = self._getResult(
            'record_score',
            {
                'game': self.game,
                'player': player,
                'category': category,
                'score': score,
            }
        )
        if result['status'] == 'OK':
            return result['key']
        else:
            raise OnlineMethodCallFailed('Could not record score: %s' % result['reason'])

    def createPlayer(self, player):
        """Creates a new player"""
        result = self._getResult(
            'create_user',
            {
                'game': self.game,
                'name': player,
            }
        )
        if result['status'] == 'OK':
            return result['key']
        else:
            raise OnlineMethodCallFailed('Could not create user: %s' % result['reason'])

    def getCategories(self):
        """Return the category names"""
        result = self._getResult(
            'get_game_categories',
            {
                'game': self.game,
            }
        )
        if result['status'] == 'OK':
            return result['categories']
        else:
            raise OnlineMethodCallFailed('Could not get categories: %s' % result['reason'])

    def getScores(self, category, player, number):
        """Return the game scores for the given category and the given player (or * for all players)"""
        result = self._getResult(
            'get_scores',
            {
                'game': self.game,
                'category': category,
                'number': number,
                'player': player,
            }
        )
        if result['status'] == 'OK':
            return result['scores']
        else:
            raise OnlineMethodCallFailed('Could not get scores: %s' % result['reason'])


class AsyncOnlineScoreTable(OnlineScoreTable):
    """Asynchronous version of the high score table

    All the methods of the high score table return futures to
    the results. If you want callbacks then you can add
    a callback to the future once you get it back.

    """

    def __init__(self, app_url, game, max_workers=1):
        """Initialise the table"""
        super(AsyncOnlineScoreTable, self).__init__(app_url, game)
        #
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers)

    def recordScore(self, player, category, score):
        """Record a score"""
        return self._executor.submit(
            super(AsyncOnlineScoreTable, self).recordScore, player, category, score)

    def createPlayer(self, player):
        """Create a new player"""
        return self._executor.submit(
            super(AsyncOnlineScoreTable, self).createPlayer, player)

    def getCategories(self):
        """Return the categories for a game"""
        return self._executor.submit(
            super(AsyncOnlineScoreTable, self).getCategories)

    def getScores(self, category, player, number):
        """Return the scores for a game"""
        return self._executor.submit(
            super(AsyncOnlineScoreTable, self).getScores, category, player, number)

    def recordScore(self, player, category, score):
        """Record the score for a game"""
        return self._executor.submit(
            super(AsyncOnlineScoreTable, self).recordScore, player, category, score)
