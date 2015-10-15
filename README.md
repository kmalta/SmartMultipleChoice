# SmartMultipleChoice

In order to accomplish our goals quickly by bootstrapping this system, 
we must disqualify ourselves from the prize money.  To put this in 
perspective, it is highly unlikely we would build a system that can achieve
top 3 leaderboard results, so this isn't unreasonable.



Web REST apis:

1. indico.io

    Documentation: https://indico.io/docs

    Request Limit: 50k per month

    Installation: 

        #requests >= 1.2.3
        $ `pip install requests`

        #six >= 1.3.0
        $ `pip install six`

        #pillow >= 2.8.1
        $ `pip install pillow`

        $ `pip install indicoio`


2. www.alchemyapi.com

    NOTE: ALCHEMY API ISN'T WORKING RIGHT NOW.  THEY CLAIM MY API KEY IS INVALID

    Documentation: http://www.alchemyapi.com/api

    Request Limit: 1k per day

    Installation:

        $ `pip install requests`


        ########## MAKE SURE THE NEXT COMMANDS ARE NOT IN OUR REPO FOLDER! ########
        ######################## PUT IT ONE DIRECTORY UP!! ########################

        If you prefer to place the files elsewhere, you must add your path to your header
        in your Python files:

        import sys
        sys.path.append('FILL_IN_PATH_HERE/alchemyapi_python')


        $ `git clone https://github.com/AlchemyAPI/alchemyapi_python.git`
        $ `cd alchemyapi_python/`

        # Fill in our API_KEY from the secrets file
        $ `python alchemyapi.py OUR_API_KEY`

        If this gives you an error, I recommend updating your python version.  I had 
        the problem where pip install verified installation of requests but I was unable
        to import the module.  EZ update fix.

        Now at the top of each python document that you will add the following:

            "from ../alchemyapi import AlchemyAPI"

        Instantiating an object is as simple as:

            "alchemyapi = AlchemyAPI()"

        Example:

            myText = "I'm excited to get started with AlchemyAPI!"
            response = alchemyapi.sentiment("text", myText)
            print "Sentiment: ", response["docSentiment"]["type"]




Gensim's python package of Word2Vec:

    Documentation: https://radimrehurek.com/gensim/models/word2vec.html

    Installation:

    Note, this may require dependencies that I am not aware of since
    I may have had them already downloaded.  This may include the package numpy.


    $ `pip install gensim`


