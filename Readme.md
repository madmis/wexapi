# Wex.nz REST API Python Client

[![Build Status][testing-image]][testing-link]
[![Coverage Status][coverage-image]][coverage-link]
[![Latest Stable Version][package-image]][package-link]
[![License][license-image]][license-link]


[Wex.nz](https://wex.nz/api/3/docs) provides REST APIs that you can use
 to interact with platform programmatically.

This API client will help you interact with Wex.nz by REST API. 


## License

MIT License


## Wex.nz REST API Reference

[Public API](https://wex.nz/api/3/docs)

[Trade API](https://wex.nz/tapi/docs)


## Contributing
To create new endpoint - [create issue](https://github.com/madmis/wexapi/issues/new) 
or [create pull request](https://github.com/madmis/wexapi/compare)


## How to use

Get ticker for each available pair (public api):

```python
conn = wexapi.common.WexConnection()
info = wexapi.public.InfoApi(conn)
api = wexapi.public.PublicApi(conn)
for pair in info.pair_names:
    ticker = api.get_ticker(pair, info)
```

Get account info (trade api - require api keys)

```python
key_file = "/var/www/keys.txt"
with wexapi.keyhandler.KeyHandler(key_file) as handler:
    if not handler.keys:
        print("No keys in key file.")
    else:
        for key in handler.keys:
            print("Printing info for key {}".format(key))

            with wexapi.WexConnection() as conn:
                t = wexapi.trade.TradeApi(key, handler, connection=conn)

                r = t.get_info()
```


## Running the tests

    python -m unittest discover wexapi


## Setup dev environment with docker

Install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

```
    cp /{proj_path}/Dockerfile.dist /{proj_path}/Dockerfile 
    cp /{proj_path}/docker-compose.yml.dist /{proj_path}/docker-compose.yml 
```

In **Dockerfile** change **{host_user}** to your local user.

Build and run docker container

```
    docker-compose build 
    docker-compose up -d 
```


## Login to docker container
```bash
    docker exec  -ti -e COLUMNS="`tput cols`" -e LINES="`tput lines`" wexapi_wexapi_1 bash
```


## Donate
If you find the library useful and would like to donate, please send some coins here:

```
BTC: 19nhMniZJ4p771ZvFHL3s8zoBML46LqFRv
BCH: qpsx260laq6wj4s99052nuy063v7j0sxsqxluur84z
ETH: 0x387D91F008dB992c7DAd9be8493dfA68E565706E
XRP: rpoi4dWSbEyQP2xmpsNMxCk2g2n5QvVSmM
Waves: 3PPXpTagbQCSXYZ3Y5h6vuFPj6RxHbnapmE
BTS: madmis-1
```


## Upgrade pip package (personal notes)
    
    python setup.py sdist
    twine upload dist/*





[testing-link]: https://travis-ci.org/madmis/wexapi
[testing-image]: https://travis-ci.org/madmis/wexapi.svg?branch=master

[coverage-link]: https://coveralls.io/github/madmis/wexapi?branch=master
[coverage-image]: https://coveralls.io/repos/github/madmis/wexapi/badge.svg?branch=master

[package-link]: https://pypi.org/project/wexapi/
[package-image]: https://img.shields.io/pypi/v/wexapi.svg?style=flat-square

[license-image]: https://img.shields.io/github/license/madmis/wexapi.svg
[license-link]: https://github.com/madmis/wexapi/blob/master/License.txt
