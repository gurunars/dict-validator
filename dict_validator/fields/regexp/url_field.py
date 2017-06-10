import re

from dict_validator.fields import StringField


PROTOCOL = r"(https?:\/\/)?"
DOMAIN = r"([\da-z\.-]+\.)+[a-z]{2,8}"
PATH = r"(\/[\/\w \.-]*)?"
QUERY = r"(\?[\/\w= \._&-]*)?"
HASH = r"(#[\/\w= \._&#-]*)?"
PORT = r"(:([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|" + \
       r"65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?"


class UrlField(StringField):
    """
    Simple pattern to match http or https URL.

    :param protocol: optional protocol spec (defaults to http[s])
    :param domain: optional domain (defaults to a wildcard)
    :param port: optional port (defaults to any number from 0 to 65535)
    :param path: optional path (defaults to a wildcard)

    >>> from dict_validator import validate

    By default a wildcard URL is matched.

    >>> class Schema:
    ...     field = UrlField()

    >>> list(validate(Schema,
    ...     {"field": "http://www.example.com/path-to-resource"
    ...               "?foo-bar=bar-foo&zoo=loo#fff-ggg"}))
    []

    SSL:

    >>> list(validate(Schema,
    ...     {"field": "https://www.example.com?foo=bar#fff"}))
    []

    With port:

    >>> list(validate(Schema,
    ...     {"field": "http://www.example.com:8080?foo=bar#fff"}))
    []

    No protocol:

    >>> list(validate(Schema,
    ...     {"field": "www.example.com?foo=bar#fff"}))
    []

    Wrong protocol:

    >>> list(validate(Schema,
    ...     {"field": "bla://www.example.com?foo=bar#fff"}))
    [(['field'], 'Did not match Regexp(url)')]

    No domain:

    >>> list(validate(Schema,
    ...     {"field": "http://foo=bar#fff"}))
    [(['field'], 'Did not match Regexp(url)')]

    It is possible to configure certain parts of the url to match specific
    values.

    >>> class Schema:
    ...     field = UrlField(protocol="ftp", domain="example.com",
    ...                      path="/foobar-zooloo", port=8080)

    >>> list(validate(Schema,
    ...     {"field": "ftp://example.com:8080/foobar-zooloo"
    ...               "?foo-bar=bar-foo&zoo=loo#fff-ggg"}))
    []

    Wrong protocol:

    >>> list(validate(Schema,
    ...     {"field": "http://example.com/foobar-zooloo?ffff#dffdf"}))
    [(['field'], 'Did not match Regexp(url)')]

    Wrong domain:

    >>> list(validate(Schema,
    ...     {"field": "ftp://not-example.com/foobar-zooloo?ffff#dffdf"}))
    [(['field'], 'Did not match Regexp(url)')]

    Wrong path:

    >>> list(validate(Schema,
    ...     {"field": "ftp://example.com/zooloo?ffff#dffdf"}))
    [(['field'], 'Did not match Regexp(url)')]

    Wrong port:

    >>> list(validate(Schema,
    ...     {"field": "ftp://example.com:100000/foobar-zooloo?ffff#dffdf"}))
    [(['field'], 'Did not match Regexp(url)')]

    """

    def __init__(self, protocol=None, domain=None, port=None,
                 path=None, *args, **kwargs):
        if port:
            port = ":" + str(port)
        else:
            port = PORT
        if protocol:
            protocol = re.escape(protocol + "://")
        else:
            protocol = PROTOCOL
        if domain:
            domain = re.escape(domain)
        else:
            domain = DOMAIN
        if path:
            path = "/" + re.escape(path.lstrip("/"))
        else:
            path = PATH
        pattern = r"^{protocol}{domain}{port}{path}{query}{hash}$".format(
            protocol=protocol, domain=domain, port=port, path=path,
            query=QUERY, hash=HASH)
        super(UrlField, self).__init__(pattern, "url", *args, **kwargs)
