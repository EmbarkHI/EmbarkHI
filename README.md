# Overview:
Embark is a webapp which plans and suggests trips based on few inputs like:
- Departure and Arrival Dates
- Budget
- Foreign/Domestic Travel
- Type of destination (Urban vs Tourist)

It uses the <a href="https://sandbox.amadeus.com/api-catalog">Amadeus API</a> to fetch the data and <a href = "http://flask.pocoo.org/"> Flask </a> to implement the backend.


# Usage
1. You must first get your Amadeus API key by registering <a href="https://sandbox.amadeus.com/">here</a>.
2. Create a config.py file with your Amadeus API key based on the example_config.py
3. Now, change directory to the location of `run.py` using the following command:
```
cd EmbarkHI
```
4. Run the app by typing:
```
python run.py
```
5. Open up your favorite browser to:
```
localhost:5000
```
6. Voila! You're good to go. 


## To do:
1. Make it faster. (Lesser queries)
2. Put it up on heroku

Graphic Attributions
  Icons from the Noun Project, licensed under the Creative Commons 3.0 License

