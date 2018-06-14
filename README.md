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

## Running the tests

    python -m unittest discover wexapi


## Upgrade pip package
    
    python setup.py sdist
    twine upload dist/*


# Login to docker container
```bash
    docker exec  -ti -e COLUMNS="`tput cols`" -e LINES="`tput lines`" wexapi_wexapi_1 bash
```


[testing-link]: https://travis-ci.org/madmis/wexapi
[testing-image]: https://travis-ci.org/madmis/wexapi.svg?branch=master

[coverage-link]: https://coveralls.io/github/madmis/wexapi?branch=master
[coverage-image]: https://coveralls.io/repos/github/madmis/wexapi/badge.svg?branch=master

[package-link]: https://pypi.org/project/wexapi/
[package-image]: https://img.shields.io/pypi/v/wexapi.svg?style=flat-square

[license-image]: https://img.shields.io/github/license/madmis/wexapi.svg
[license-link]: https://github.com/madmis/wexapi/blob/master/LICENSE.TXT
