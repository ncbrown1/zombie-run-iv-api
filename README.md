# Zombie Run IV API

This is a Python Flask web server using Flask-Restful to serve a REST API for the Zombie Run IV Unity game. The API lays on top of the game's database in order to provide operations on the universal data set, such as the list of high scores. We also keep track of individual player statistics and fields, such as powerup level, high five count, and number of unlocked characters. This allows for persistence of game data without having to rely on each computer's local storage.

There is no authentication or authorization set up with this API. We are relying on the "honor system", in that we trust our users to use this resource wisely and fairly. Security and penetration testing is not within the scope of this project and as such will not be implemented in the final deliverable in March 2016. If, for any reason, we decide to move forward with this game, these topics will be important and will need to be developed. Contributions are welcome!

There is code written in C# that consumes this API, located [in this other repository](https://github.com/ncbrown1/zombie-run-iv-api-client). That code is meant to be injected into a Unity (or possibly Unreal Engine) game project so that the game will have access to this API and its data.

## Requirements

* SQLite3
* Python 2.7
* (optional) Postgresql

## Testing

Tests are currently located in `test.py`. You can run them as follows:
1. Clone (or Fork + Clone) this repository
1. Create a virtualenv, activate it, and install the requirements.txt
1. Run the tests via `python test.py`
```
  $ virtualenv env
  $ source env/bin/activate
  $ pip install -r requirements.txt
  $ python test.py
```

This creates a test database for each unit test and runs them. A `.` corresponds to a passing test case. An `F` corresponds to a failing test case, which will show the failing test output at the bottom.


## Deployment

1. Clone (or Fork + Clone) this repository
1. Create a virtualenv, activate it, and install the requirements.txt
1. Run the server
```bash
  $ virtualenv env
  $ source env/bin/activate
  $ pip install -r requirements.txt
  $ python manage.py runserver
```

If you want to reset the database, do the following
```bash
rm zriv.db
echo 'db.create_all()' | python manage.py shell
```

To deploy on Heroku, simply fork this repo and point your new Heroku app at your forked repository and deploy the master branch. Before you can use it, however, you must `heroku run echo 'db.create_all()' | python manage.py shell` if you don't have the zriv.db file in the github repository.

## API Routes

#### GET /players
  * Corresponding function: app/api/players.py:get_players
  * Parameters: None
  * Request arguments: None
  * Response: 200 OK and a json array of all registered players in game DB
  * Sample response:
```javascript
{
  "players": [
    {
      "characters": 1,
      "hifive_count": 0,
      "id": 1,
      "name": "nick",
      "powerup_lvl": 1,
      "scores": [
        {
          "score": 123,
          "time": "Sat, 20 Feb 2016 20:43:36 -0000"
        },
        {
          "score": 12,
          "time": "Sat, 20 Feb 2016 20:44:01 -0000"
        }
      ]
    },
    {
      "characters": 1,
      "hifive_count": 0,
      "id": 2,
      "name": "steve",
      "powerup_lvl": 1,
      "scores": [
        {
          "score": 1338,
          "time": "Sat, 20 Feb 2016 22:13:11 -0000"
        }
      ]
    }
  ]
};
```

#### GET /players/:id
  * Corresponding function: app/api/players.py:get_player
  * Parameters:
    * id: (integer) A valid Player ID
  * Request arguments: None
  * Response:
    * Error 404 and `{"error": "Not found."}` if no player with the given ID exists.
    * Otherwise 200 OK and json object for respective player
  * Sample response: (GET /players/2)
```javascript
{
  "characters": 1,
  "hifive_count": 0,
  "id": 2,
  "name": "steve",
  "powerup_lvl": 1,
  "scores": [
    {
      "score": 1338,
      "time": "Sat, 20 Feb 2016 22:13:11 -0000"
    }
  ]
}
```

#### GET /players/find
  * Corresponding function: app/api/players.py:find_player
  * Parameters: None
  * Request arguments:
    * device_id: (string) The UUID of the device a player is registered with
    * name: (string) The name of the player
  * Response:
    * Error 404 and `{"error": "Not found."}` if no player with that name and device_id exists.
    * Error 400 if arguments are incorrect or not present.
    * Otherwise 200 OK and a json object of the first player result of query
  * Sample response: (GET /players/find?name=nick&device_id=abc123)
```javascript
{
  "characters": 1,
  "hifive_count": 0,
  "id": 1,
  "name": "nick",
  "powerup_lvl": 1,
  "scores": [
    {
      "score": 123,
      "time": "Sat, 20 Feb 2016 20:43:36 -0000"
    },
    {
      "score": 12,
      "time": "Sat, 20 Feb 2016 20:44:01 -0000"
    }
  ]
}
```

#### POST /players
  * Corresponding function: app/api/players.py:create_player
  * Parameters: None
  * Request arguments:
    * device_id: (string) The UUID of the device a player is registering with
    * name: (string) The name of the player
  * Response:
    * Error 400 if arguments are incorrect or not present.
    * A new player json object with given name and device_id, and with default values for all other fields
    * If a player with the name and device_id given already exists, that player is returned
    * 200 OK if success
  * Sample response: (POST /players/find?name=nick&device_id=abc123)
```javascript
{
  "characters": 1,
  "hifive_count": 0,
  "id": 1,
  "name": "nick",
  "powerup_lvl": 1,
  "scores": [
    {
      "score": 123,
      "time": "Sat, 20 Feb 2016 20:43:36 -0000"
    },
    {
      "score": 12,
      "time": "Sat, 20 Feb 2016 20:44:01 -0000"
    }
  ]
}
```

#### [POST, PUT] /players/:id/hifives
  * Corresponding function: app/api/players.py:set_hifives
  * Parameters:
    * id: (integer) A valid Player ID
  * Request arguments:
    * hifives: (integer) The new number of hifives player (:id) should have
  * Response:
    * Error 404 and `{"error": "Not found."}` if no player with the given ID exists.
    * Error 400 if arguments are incorrect or not present.
    * Otherwise, 200 OK and json object of respective player is returned with new hifive_count value.
  * Sample response: (POST /players/2/hifives?hifives=42)
```javascript
{
  "characters": 1,
  "hifive_count": 42,
  "id": 2,
  "name": "steve",
  "powerup_lvl": 1,
  "scores": [
    {
      "score": 1338,
      "time": "Sat, 20 Feb 2016 22:13:11 -0000"
    }
  ]
}
```

#### [POST, PUT] /players/:id/characters
  * Corresponding function: app/api/players.py:set_characters
  * Parameters:
    * id: (integer) A valid Player ID
  * Request arguments:
    * characters: (integer) The new character number player (:id) should have
  * Response:
    * Error 404 and `{"error": "Not found."}` if no player with the given ID exists.
    * Error 400 if arguments are incorrect or not present.
    * Otherwise, 200 OK and json object of respective player is returned with new characters value.
  * Sample response: (POST /players/2/characters?characters=7)
```javascript
{
  "characters": 7,
  "hifive_count": 42,
  "id": 2,
  "name": "steve",
  "powerup_lvl": 1,
  "scores": [
    {
      "score": 1338,
      "time": "Sat, 20 Feb 2016 22:13:11 -0000"
    }
  ]
}
```

#### GET /players/:id/scores
  * Corresponding function: app/api/players.py:get_player_scores
  * Parameters:
    * id: (integer) A valid Player ID
  * Request arguments:
    * limit: (integer, optional, default=15) The maximum number of score entries to return
  * Response:
    * Error 404 and `{"error": "Not found."}` if no player with the given ID exists.
    * Otherwise, 200 OK and list of scores for player (:id)
  * Sample response: (GET /players/1/scores?limit=4)
```javascript
{
  "scores": [
    {
      "player": {
        "name": "nick"
      },
      "score": 1337,
      "time": "Sat, 20 Feb 2016 22:12:25 -0000"
    },
    {
      "player": {
        "name": "nick"
      },
      "score": 123,
      "time": "Sat, 20 Feb 2016 20:43:36 -0000"
    },
    {
      "player": {
        "name": "nick"
      },
      "score": 17,
      "time": "Sat, 20 Feb 2016 20:44:06 -0000"
    },
    {
      "player": {
        "name": "nick"
      },
      "score": 12,
      "time": "Sat, 20 Feb 2016 20:44:01 -0000"
    }
  ]
}
```

#### GET /scores
  * Corresponding function: app/api/scores.py:get_scores
  * Parameters: None
  * Request arguments:
    * limit: (integer, optional, default=15) The maximum number of score entries to return
  * Response:
    * 200 OK and a json array of `limit` top high scores for entire game.
  * Sample response:
```javascript
{
  "scores": [
    {
      "player": {
        "name": "steve"
      },
      "score": 1338,
      "time": "Sat, 20 Feb 2016 22:13:11 -0000"
    },
    {
      "player": {
        "name": "nick"
      },
      "score": 1337,
      "time": "Sat, 20 Feb 2016 22:12:25 -0000"
    },
    {
      "player": {
        "name": "nick"
      },
      "score": 123,
      "time": "Sat, 20 Feb 2016 20:43:36 -0000"
    },
    {
      "player": {
        "name": "nick"
      },
      "score": 17,
      "time": "Sat, 20 Feb 2016 20:44:06 -0000"
    },
    {
      "player": {
        "name": "nick"
      },
      "score": 12,
      "time": "Sat, 20 Feb 2016 20:44:01 -0000"
    }
  ]
}
```

#### POST /scores
  * Corresponding function: app/api/scores.py:create_score
  * Parameters: None
  * Request arguments:
    * device_id: (string) The UUID of the device this score was achieved on
    * name: (string) The name of the player that achieved this score
    * score: (integer) The score being recorded
  * Response:
    * Error 400 if arguments are incorrect or not present.
    * Otherwise, 200 OK and a json object representing the new score
    * If no user with `device_id` and `name` existed before this request, that player is created.
  * Sample response: (POST /scores?name=steve&device_id=xyz567&score=71)
```javascript
{
  "player": {
    "name": "steve"
  },
  "score": 71,
  "time": "Sat, 20 Feb 2016 20:48:04 -0000"
}
```

## Roadmap
* ~~Unit Testing :: Done March 8, 2016~~

## Credits
Thanks to @colekettler for the [Flask REST API Generator](https://github.com/colekettler/generator-flask-api), which provided this project with the initial project scaffolding.

## License
Licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Support
Please use GitHub issues for support requests.
