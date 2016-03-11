import os
import sys
from app import create_app, db
import unittest
from threading import Thread
from flask.ext.sqlalchemy import SQLAlchemy
import json
from itertools import izip, islice
from random import randint

DEVICEID = 'abc123'
NAMES = ['alice','bob','charlie','doug','erica','francis','greg','henry','ian','john','karen','lauren','megan','nick','oliver','peter','quentin','ryan','steven','tracy','uriel','veronica','wendy','young','zane']

class ApiTestCases(unittest.TestCase):

    def setUp(self):
        self.flapp = create_app('testing')
        self.app = self.flapp.test_client()
        # self.db.session.expire_all()
        # self.db.drop_all()
        db.init_app(self.flapp)
        with self.flapp.app_context():
            db.create_all()

    def tearDown(self):
        with self.flapp.app_context():
            db.drop_all()
        # os.unlink(self.sqlitedb)

    def test_passing(self):
        """
        At least one unit test should pass
        """
        self.assertEqual(1,1)

    def test_failing(self):
        """
        At least one unit test should fail
        """
        self.assertEqual(1,2)

    ###########################################################################
    # ROOT TEST CASES
    ###########################################################################

    def test_get_root(self):
        """
        The root of the website should return some statically specified data.
        """
        rv = self.app.get('/')
        self.assertIn('Hello, world!', rv.data)

    ###########################################################################
    # PLAYERS TEST CASES
    ###########################################################################

    def test_players_is_initially_empty(self):
        """
        On initial app, there should be no players.
        """
        rv = self.app.get('/players')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('players', data)
        self.assertEqual(data['players'], [])

    def test_bad_add_player1(self):
        """
        The app should make sure the proper parameters are passed in when creating a player.
        """
        rv = self.app.post('/players')
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_player2(self):
        """
        The app should make sure the proper parameters are passed in when creating a player.
        """
        rv = self.app.post('/players?name=testuser')
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_player3(self):
        """
        The app should make sure the proper parameters are passed in when creating a player.
        """
        rv = self.app.post('/players?device_id=%s' % DEVICEID)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_add_player(self):
        """
        The app should create a player when the proper parameters are passed in.

        This test can be called by other tests to insert and return a new player into the database with name 'testuser' and device_id `DEVICEID`
        """
        rv = self.app.post('/players?name=testuser&device_id=%s' % DEVICEID)
        self.assertEqual(rv.status_code, 200)
        player = json.loads(rv.data)
        self.assertIn('id', player)
        self.assertIn('name', player)
        self.assertEqual(player['name'], 'testuser')

        return player

    def test_add_check_all_players(self):
        """
        The app should maintain information about players after they are created.
        """
        # create the user first
        self.test_add_player()

        rv = self.app.get('/players')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('players', data)
        self.assertEqual(len(data['players']), 1)
        player = data['players'][0]
        self.assertEqual(player['name'], 'testuser')
        self.assertEqual(player['hifive_count'], 0)
        self.assertEqual(player['characters'], 1)
        self.assertEqual(player['powerup_lvl'], 1)

    def test_add_check_player(self):
        """
        The app should maintain information about players after they are created.
        """
        # create the user first
        player = self.test_add_player()

        _id = player['id']
        rv = self.app.get('/players/%d' % _id)
        self.assertEqual(rv.status_code, 200)
        retplayer = json.loads(rv.data)
        self.assertIn('id', retplayer)
        self.assertIn('name', retplayer)
        self.assertIn('hifive_count', retplayer)
        self.assertIn('characters', retplayer)
        self.assertIn('powerup_lvl', retplayer)

        self.assertEqual(retplayer['id'], player['id'])
        self.assertEqual(retplayer['name'], player['name'])
        self.assertEqual(retplayer['hifive_count'], player['hifive_count'])
        self.assertEqual(retplayer['characters'], player['characters'])
        self.assertEqual(retplayer['powerup_lvl'], player['powerup_lvl'])

    def test_player_id_not_found(self):
        """
        The app should return 404 if a player is not found when retrieving by id.
        """
        rv = self.app.get('/players/1')
        self.assertEqual(rv.status_code, 404)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_find_player1(self):
        """
        The app should make sure the proper parameters are passed in when finding a player.
        """
        rv = self.app.get('/players/find')
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_find_player2(self):
        """
        The app should make sure the proper parameters are passed in when finding a player.
        """
        rv = self.app.get('/players/find?name=%s' % 'test')
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_find_player3(self):
        """
        The app should make sure the proper parameters are passed in when finding a player.
        """
        rv = self.app.get('/players/find?device_id=%s' % DEVICEID)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_not_found_player(self):
        """
        The app should make sure the proper parameters are passed in when finding a player.
        """
        rv = self.app.get('/players/find?name=%s&device_id=%s' % ('testuser',DEVICEID))
        self.assertEqual(rv.status_code, 404)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_find_player(self):
        """
        If a player exists, the app should return that player when searching with the player's name and device_id.
        """
        player = self.test_add_player()
        name = player['name']

        rv = self.app.get('/players/find?name=%s&device_id=%s' % (name, DEVICEID))
        self.assertEqual(rv.status_code, 200)
        retplayer = json.loads(rv.data)
        self.assertIn('id', retplayer)
        self.assertIn('name', retplayer)
        self.assertIn('hifive_count', retplayer)
        self.assertIn('characters', retplayer)
        self.assertIn('powerup_lvl', retplayer)

        self.assertEqual(retplayer['id'], player['id'])
        self.assertEqual(retplayer['name'], player['name'])
        self.assertEqual(retplayer['hifive_count'], player['hifive_count'])
        self.assertEqual(retplayer['characters'], player['characters'])
        self.assertEqual(retplayer['powerup_lvl'], player['powerup_lvl'])

    def test_bad_set_player_hifives1(self):
        """
        The app should make sure the proper parameters are passed in when updating the hifive_count
        """
        player = self.test_add_player()
        _id = player['id']
        rv = self.app.post('/players/%d/hifives' % _id)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_set_player_hifives2(self):
        """
        The app should make sure the proper parameters are passed in when updating the hifive_count
        """
        player = self.test_add_player()
        _id = player['id']
        rv = self.app.post('/players/%d/hifives?hifives=abc' % _id)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_set_player_hifives3(self):
        """
        The app should return 404 if the player is not found when updating the hifive_count.
        """
        rv = self.app.post('/players/1/hifives')
        self.assertEqual(rv.status_code, 404)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_set_player_hifives(self):
        """
        The app should update a player's hifive_count if the proper parameters are passed in.
        """
        player = self.test_add_player()
        _id = player['id']

        new_val = 42
        rv = self.app.post('/players/%d/hifives?hifives=%d' % (_id, new_val))
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('id', data)
        self.assertEqual(data['id'], _id)
        self.assertIn('hifive_count', data)
        self.assertEqual(data['hifive_count'], new_val)

    def test_bad_set_player_characters1(self):
        """
        The app should make sure the proper parameters are passed in when updating the characters
        """
        player = self.test_add_player()
        _id = player['id']
        rv = self.app.post('/players/%d/characters' % _id)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_set_player_characters2(self):
        """
        The app should make sure the proper parameters are passed in when updating the characters
        """
        player = self.test_add_player()
        _id = player['id']
        rv = self.app.post('/players/%d/characters?hifives=abc' % _id)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_set_player_characters3(self):
        """
        The app should return 404 if the player is not found when updating the characters.
        """
        rv = self.app.post('/players/1/characters')
        self.assertEqual(rv.status_code, 404)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_set_player_characters(self):
        """
        The app should update a player's characters if the proper parameters are passed in.
        """
        player = self.test_add_player()
        _id = player['id']

        new_val = 42
        rv = self.app.post('/players/%d/characters?characters=%d' % (_id, new_val))
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('id', data)
        self.assertEqual(data['id'], _id)
        self.assertIn('characters', data)
        self.assertEqual(data['characters'], new_val)

    def test_bad_set_player_poweruplvl1(self):
        """
        The app should make sure the proper parameters are passed in when updating the powerup_lvl
        """
        player = self.test_add_player()
        _id = player['id']
        rv = self.app.post('/players/%d/powerup_lvl' % _id)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_set_player_poweruplvl2(self):
        """
        The app should make sure the proper parameters are passed in when updating the powerup_lvl
        """
        player = self.test_add_player()
        _id = player['id']
        rv = self.app.post('/players/%d/powerup_lvl?powerup_lvl=abc' % _id)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_set_player_poweruplvl3(self):
        """
        The app should return 404 if the player is not found when updating the powerup_lvl.
        """
        rv = self.app.post('/players/1/powerup_lvl')
        self.assertEqual(rv.status_code, 404)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_set_player_poweruplvl(self):
        """
        The app should update a player's powerup_lvl if the proper parameters are passed in.
        """
        player = self.test_add_player()
        _id = player['id']

        new_val = 42
        rv = self.app.post('/players/%d/powerup_lvl?powerup_lvl=%d' % (_id, new_val))
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('id', data)
        self.assertEqual(data['id'], _id)
        self.assertIn('powerup_lvl', data)
        self.assertEqual(data['powerup_lvl'], new_val)

    def test_bad_get_player_scores1(self):
        """
        The app should return 404 if the player is not found when retrieving their scores.
        """
        rv = self.app.get('/players/1/scores')
        self.assertEqual(rv.status_code, 404)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_player_scores_initially_empty(self):
        """
        On initial player creation, there should be no scores.
        """
        player = self.test_add_player()
        _id = player['id']

        rv = self.app.get('/players/1/scores')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('scores', data)
        self.assertEqual(data['scores'],[])

    ###########################################################################
    # SCORES TEST CASES
    ###########################################################################

    def test_get_scores_initially_empty(self):
        """
        On initial app, there should be no scores.
        """
        player = self.test_add_player()
        _id = player['id']

        rv = self.app.get('/scores')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('scores', data)
        self.assertEqual(data['scores'],[])

    def test_bad_add_score1(self):
        """
        The app should make sure the proper parameters are passed in when creating a new score.
        """
        rv = self.app.post('/scores')
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_score2(self):
        """
        The app should make sure the proper parameters are passed in when creating a new score.
        """
        rv = self.app.post('/scores?device_id=%s' % DEVICEID)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_score3(self):
        """
        The app should make sure the proper parameters are passed in when creating a new score.
        """
        rv = self.app.post('/scores?name=%s' % 'testuser')
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_score4(self):
        """
        The app should make sure the proper parameters are passed in when creating a new score.
        """
        rv = self.app.post('/scores?score=%d' % 1)
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_score5(self):
        """
        The app should make sure the proper parameters are passed in when creating a new score.
        """
        rv = self.app.post('/scores?device_id=%s&name=%s' % (DEVICEID, 'testuser'))
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_score6(self):
        """
        The app should make sure the proper parameters are passed in when creating a new score.
        """
        rv = self.app.post('/scores?score=%d&name=%s' % (2, 'testuser'))
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_bad_add_score7(self):
        """
        The app should make sure the proper parameters are passed in when creating a new score.
        """
        rv = self.app.post('/scores?device_id=%s&score=%d' % (DEVICEID, 3))
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.data)
        self.assertIn('error', data)

    def test_add_score(self, name='testuser', score=1):
        """
        The app should create a new score when all the proper parameters are passed in. If the player with the given name did not exist yet, it should exist after the create-score call.
        """
        rv = self.app.post('/scores?device_id=%s&name=%s&score=%d' % (DEVICEID, name, score))
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('rank', data)
        self.assertIn('score', data)
        self.assertIn('player', data['score'])
        self.assertIn('name', data['score']['player'])
        self.assertIn('score', data['score'])

        self.assertEqual(data['score']['score'], score)
        self.assertEqual(data['score']['player']['name'], name)

        rv = self.app.get('/players')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('players', data)
        self.assertGreaterEqual(len(data['players']), 1)
        found = False
        for player in data['players']:
            self.assertIn('name', player)
            self.assertIn('scores', player)
            if player['name'] == name:
                found = True
                foundScore = False
                for s in player['scores']:
                    self.assertIn('score', s)
                    if s['score'] == score:
                        foundScore = True
                self.assertTrue(foundScore)
        self.assertTrue(found)

    def test_add_multiple_scores(self):
        """
        The app should maintain information about multiple scores.
        """
        for i in range(50):
            name = NAMES[randint(0,len(NAMES)-1)]
            self.test_add_score(name=name,score=randint(10,10000))

        rv = self.app.get('/scores')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('scores', data)
        self.assertLessEqual(len(data['scores']), 15)

        for fst, snd in izip(data['scores'], islice(data['scores'], 1, None)):
            self.assertLessEqual(snd['score'], fst['score'], msg="Scores not in decreasing order")

    def test_limit_get_scores(self):
        """
        The app should maintain information about multiple scores.
        """
        for i in range(50):
            name = NAMES[randint(0,len(NAMES)-1)]
            self.test_add_score(name=name,score=randint(10,10000))

        rv = self.app.get('/scores?limit=3')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('scores', data)
        self.assertLessEqual(len(data['scores']), 3)

        for fst, snd in izip(data['scores'], islice(data['scores'], 1, None)):
            self.assertLessEqual(snd['score'], fst['score'], msg="Scores not in decreasing order")

    def test_multiple_player_scores(self):
        """
        The app should return data about player scores and should be limited with default of 15.
        """
        for i in range(50):
            name = 'testuser'
            self.test_add_score(name=name,score=randint(10,10000))

        rv = self.app.get('/scores')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('scores', data)
        self.assertLessEqual(len(data['scores']), 15)

        for fst, snd in izip(data['scores'], islice(data['scores'], 1, None)):
            self.assertLessEqual(snd['score'], fst['score'], msg="Scores not in decreasing order")

    def test_limit_player_scores(self):
        """
        The app should return data about player scores and should be limited with default of 15.
        """
        for i in range(50):
            name = 'testuser'
            self.test_add_score(name=name,score=randint(10,10000))

        rv = self.app.get('/scores?limit=3')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertIn('scores', data)
        self.assertLessEqual(len(data['scores']), 3)

        for fst, snd in izip(data['scores'], islice(data['scores'], 1, None)):
            self.assertLessEqual(snd['score'], fst['score'], msg="Scores not in decreasing order")

if __name__ == '__main__':
    unittest.main()
