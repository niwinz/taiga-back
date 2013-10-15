To login you have to send a POST to this endpoint with a json with the keys email and password, for example::

  {"username": "my-user-name", "password": "my-secret-password"}

If the login fails the response will be a 404 with the error message in the body, for example::

  { "detail": "username does not match any user" }

if the login is correct the response will be a 200 with the user data and a token in the body, for example::

  {
      "id": 1,
      "username": "my-user-name",
      "first_name": "",
      "last_name": "",
      "email": "john@doe.com",
      "color": "",
      "description": "",
      "default_language": "",
      "default_timezone": "",
      "is_active": true,
      "photo": "",
      "projects": [
          1,
          2,
          3
      ],
      "token": "t5sa7aod1c9w4mwh091yorv1whqub6yg"
  }

To use this login session you have to send the token in every request in the X-SESSION-TOKEN HTTP header.
