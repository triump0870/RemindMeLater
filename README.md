# [Remind Me Later][0]
----------------

RemindMeLater is a webapp which reminds user at user's specified time. Anybody can open the webapp, provide either their email address or their mobile number or both and setup a reminder with a message. RemindMeLater then reminds them over their preferred channel of notification with the message.

This project has the following basic apps:

* API -- This app handles all the API requests and responses
* Reminder -- This app represents all the Reminder objects
* Account -- This app handles the user logins and registrations
* Profile -- This app is for personalizing the user profile

## Installation

### Quick start

To set up a development environment quickly, first install Python. Setup a virtual environent. Then
1. `$ git clone https://github.com/triump0870/RemindMeLater.git`

Install all dependencies:

`pip install -r requirements.txt`

Run migrations:

`python src/manage.py migrate`

### Detailed instructions

Take a look at the docs for more information.

[0]: https://remind-me-later.herokuapp.com/apis/remiders
=======
