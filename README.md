# Meteorological data API

## How to run

- Create a virtual environment `python3 -m venv .venv` (optional)
  - Activate the virtual environment `source .venv/bin/activate`
- Install all dependencies by running `pip install -r requirements.txt`
- Copy your AEMET API key to the `API_KEY` variable in the .env file
- Run the Meteorological API service with `python main.py`
- Send a request to the API for example using the following curl command: `curl --location 'http://localhost:5000/aemet/start_time/2025-02-01T00:00:00UTC/end_time/2025-02-01T23:50:00UTC/station/89070?agg=hourly'`

## Todos left

- Do input validation of query parameters e.g. ignore all values other than 'temp', 'pres', 'vel'
- Check for each new request whether the data for the whole time range is already stored in the DB. If not, fetch the missing data from the API and store it.
- Add more exception handling for different kinds of exceptions
- Add more test coverage
- Integration tests for DB queries
- Add a front end

## Discussion

- Use of metrics and alerts
  - Application specific metrics can be defined in the application code and exposed (e.g. to Prometheus). These are usually quantifiable values that are important and should be observed. This could be for example the average response time. If that metric exceeds a certain value, then an alert could notify the team so that they can investigate why the response time has increased.
- How to avoid unnecessary requests from data consumers if data updates happen a few times per day?
  - Caching of data can avoid unnecessary requests to the data source. If the data only updates few times per day then the cached data can also be updated in intervals and this data is used to serve the data consumers.
- Find ways to improve the handling of the income request of the users
  - The requests of the users should be validated. Any invalid request should have the appropriate "Bad Request" status code. Also in this way SQL injection or other malicious input should be avoided.
  - Ensure that requests have a maximum timeout. Do not allow that requests take longer than a certain amount of time.
- What other things we could expand the service to provide more value to the user?
  - For faster responses load more data in the background so that more data is cached. Eventually download the whole dataset.
  - Show the user how many requests they already did.
- How should we do AuthZ/AuthN? What trade-offs do you see?
  - AuthN
    - A simple AuthN could be to provide API keys to the user which they can use for each request.
      - That is not a very safe AuthN as an API key can get lost or can get stolen
      - They are simple to use for the user
    - An alternative would be Json Web Tokens. 
      - JWTs have improved security as they usually expire after a certain amount of time. Then a new JWT needs to be generated. So there is a limited security risk in case somebody "steals" the JWT
      - These tokens are digitally signed. Changing the JWT makes it invalid.
  - AuthZ
    - API keys can have a defined capability. Each time a user uses them, this capability has to be somehow checked with a possible DB request in the backend. That can potentially have a performance cost.
    - JWTs contain the resources the user has permission to use. That makes it very efficient as the backend doesn't need to check what authorizations this user has, because they're already in the token. That works only because these tokens are digitally signed and therefore temper-proof.