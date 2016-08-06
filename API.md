API Documentation
------------------------
This is the API documentation of **RemindMeLater** App.
The API provides endpoints for creatting a reminder and accessing the reminder for updatation and deletion. It can be accessed via a simple API call.

The API defines the following endpoint:

> * https://remind-me-later.herokuapp.com/apis/reminders


API request
-----------

    
>   curl -H "Content-Type: application/json" -X POST http://remind-me-later.herokuapp.com/apis/reminders -d '{"message":"The message","date":"2016-08-06","time":"17:40:10","phone_number":"+919876543210","email":"example@example.com"}'


The JSON object returned looks like:

    {
        "id": 4,
        "task_id": "3831b77f-2968-4108-8046-b33033380cd1",
        "message": "The message",
        "phone_number": "+919876543210",
        "email": "example@example.com",
        "date": "2016-08-06",
        "time": "17:40:10",
        "completed": false
    }

In case of a successful task execution by celery, the `completed` field gets changed to `true`.

    {
        "id": 4,
        "task_id": "3831b77f-2968-4108-8046-b33033380cd1",
        "message": "The message",
        "phone_number": "+919876543210",
        "email": "example@example.com",
        "date": "2016-08-06",
        "time": "17:40:10",
        "completed": true
    }
    
