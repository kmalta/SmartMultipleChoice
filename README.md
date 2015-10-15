# SmartMultipleChoice

In order to accomplish our goals quickly by bootstrapping this system, 
we must disqualify ourselves from the prize money.  To put this in 
perspective, it is highly unlikely we would build a system that can achieve
top 3 leaderboard results, so this isn't unreasonable.



Web REST apis:

1. www.alchemyapi.com

    Documentation: http://www.alchemyapi.com/api

    Installation:

    $ `pip install requests`


    ########## MAKE SURE THE NEXT COMMANDS ARE NOT IN OUR REPO FOLDER! ########
    ######################## PUT IT ONE DIRECTORY UP!! ########################


    $ `git clone https://github.com/AlchemyAPI/alchemyapi_python.git`
    $ `cd alchemyapi_python/`

    # Fill in our API_KEY from the secrets file
    $ `python alchemyapi.py OUR_API_KEY`

    If this gives you an error, I recommend updating your python version.  I had 
    the problem where pip install verified installation of requests but I was unable
    to import the module.  EZ update fix.

    Now at the top of each python document that you will add the following:

        "from alchemyapi import AlchemyAPI"

    Instantiating an object is as simple as:

        "alchemyapi = AlchemyAPI()"

    Example:

        myText = "I'm excited to get started with AlchemyAPI!"
        response = alchemyapi.sentiment("text", myText)
        print "Sentiment: ", response["docSentiment"]["type"]

