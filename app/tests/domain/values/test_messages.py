import pytest
from app.domain.values.messages import Text
from mimesis import Text as MimesisText

def test_create_message_success():
    text = Text("")
