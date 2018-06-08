import decimal
import http.client as client
import json
import typing


def parse_json_response(response: typing.Union[str, client.HTTPResponse]) -> dict:
    def parse_decimal(var):
        return decimal.Decimal(var)

    try:
        if type(response) is not str:
            response_data = response.read().decode('utf-8')
        else:
            response_data = response

        r = json.loads(response_data, parse_float=parse_decimal, parse_int=parse_decimal)
    except Exception as e:
        msg = "Error while attempting to parse JSON response: %s\nResponse:\n%r" % (e, response)
        raise Exception(msg)

    return r


def truncate_amount_digits(
        value: typing.Union[float, int, str, decimal.Decimal],
        digits: int,
) -> decimal.Decimal:
    """
    :param value: int|float|str|decimal.Decimal
    :param digits:
    :return: Decimal
    """
    quanta = [decimal.Decimal("1e-%d" % i) for i in range(16)]

    if type(value) is int:
        value = str(value)

    if type(value) is float:
        value = str(value)

    if type(value) is str:
        value = decimal.Decimal(value)

    quantum = quanta[int(digits)]

    return value.quantize(quantum)


def format_currency_digits(
        value: typing.Union[float, int, str, decimal.Decimal],
        digits: int,
) -> str:
    """
    :param value: int|float|str|decimal.Decimal
    :param digits:
    :return: str
    """
    return str(truncate_amount_digits(value, digits))


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))
