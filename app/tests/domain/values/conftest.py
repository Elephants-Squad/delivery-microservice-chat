from mimesis import Text as MimesisText
from pytest import fixture


@fixture(scope='module')
def mimesis_object():
    return MimesisText()
