from dotenv import load_dotenv
from src.api.api import app
import logging

def main():
    # main driver function
    load_dotenv()
    app.logger.setLevel(logging.INFO)

    app.logger.info('Starting API')

        # run() method of Flask class runs the application
        # on the local development server.
    app.run(debug=True)


if __name__ == '__main__':
    main()
