# credit-suisse-it


Welcome to CodeIT Suisse 2016!
Gather around as a team and read this!

What to do
The aim is to create an application together as a team and make as much money as you can, as quick as you can!
Throughout Saturday, you are free to play with the testing servers however you like. If you run out of money during this test phase, just let us know! -- We are here to help in any way we can!
On Sunday, you will run your final application and see if you can outsmart the other teams around you!

Your team
You team will start off with 1 million in your account that you are free to use how you like.

Where to begin?
To start, our servers first need to know who you and your team are!
Spend one or two minutes to think up a team name amongst you and using any method you wish, start by performing an HTTP POST request to the following URL:

http://cis2016-teamtracker.herokuapp.com/api/teams
Provide any missing information that it may need in the body as json.
When your team is created, please store your secret UID that is generated for your team - you will need this later!
Once you have this ID, validate your secret team UID by visiting the following URL:

http://cis2016-teamtracker.herokuapp.com/api/teams/validate/{TEAM UID}
Once this is successful, check the dashboard on the big screens - this should update and show you have completed the first stage! - Give a loud cheer to show the other teams that you have done it!
Continue to complete the other stages by following the instructions provided when you successfully validated your team!
If at any stage, you wish to view the next stage hint, append '?next_steps' to any of the endpoints you have gathered over time. Once you have all the endpoints collected, this will not need to be appended.
On behalf of everyone here, we wish you the very best of luck!
Remember, reach out to any of us identified by a blue line on our name badges if you encounter any problems or have any questions and we will try our best to help out where we can!


{"status":"Success. Team created. Please keep the following UID private, as this is used to identify your team in API requests.","uid":"WQKW1pUQiKdCw7TIzBnWwg"}

1. http://cis2016-teamtracker.herokuapp.com/api/teams/WQKW1pUQiKdCw7TIzBnWwg?next_stage
2. http://cis2016-exchange1.herokuapp.com/api/market_data/0001
3. http://cis2016-exchange1.herokuapp.com/api/orders?next_stage
4. http://cis2016-teamtracker.herokuapp.com/summary/WQKW1pUQiKdCw7TIzBnWwg

"message": "team_uid can't be blank, side can't be blank, side is incorrect. Can only be 'buy' or 'sell', qty can't be blank, order_type can't be blank, order_type is incorrect. Can only be 'market' or 'limit'",


{"id":"7155bed1-5273-477b-8512-a6593093b36c","team_uid":"WQKW1pUQiKdCw7TIzBnWwg","symbol":"0005","side":"buy","qty":1,"order_type":"market","price":null,"status":"FILLED","filled_qty":1}

{"id":"2187c7bb-c4ce-4321-8e04-cdc8b7b3bb35","team_uid":"WQKW1pUQiKdCw7TIzBnWwg","symbol":"0005","side":"sell","qty":1,"order_type":"market","price":null,"status":"FILLED","filled_qty":1}
