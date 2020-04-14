# planet-Express-abe

planet-express-abe is the API-REST module of Planet express project, It's works
with flask and mongodb.

## Installation

We install the python libraries from requiriments.txt with pip, we use python3
```bash
pip install -r requirements.txt
```

For development purposes, we include a docker-compose with mongodb and rabbitmq
docker images and a docker network to comunicate with other modules of
planet express.
```bash
docker-compose up
```

## Usage

To run the API-REST
```python
cd src && python api_rest.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
