import re

from dataclasses import dataclass
from app.domain.values.base import BaseValueObject
from app.domain.exceptions import TextTooLongException, ObsceneTextException, EmptyTextException
from typing import NoReturn, Final

pattern: Final[str] = r"""
(?iux)(?<![а-яё])(?:
(?:(?:у|[нз]а|(?:хитро|не)?вз?[ыьъ]|с[ьъ]|(?:и|ра)[зс]ъ?|(?:о[тб]|п[оа]д)[ьъ]?|(?:\S(?=[а-яё]))+?[оаеи-])-?)?(?:
  [её](?:б(?!о[рй]|рач)|п[уа](?:ц|тс))|
  и[пб][ае][тцд][ьъ]
).*?|

(?:(?:н[иеа]|(?:ра|и)[зс]|[зд]?[ао](?:т|дн[оа])?|с(?:м[еи])?|а[пб]ч|в[ъы]?|пр[еи])-?)?ху(?:[яйиеёю]|л+и(?!ган)).*?|

бл(?:[эя]|еа?)(?:[дт][ьъ]?)?|

\S*?(?:
  п(?:
    [иеё]зд|
    ид[аое]?р|
    ед(?:р(?!о)|[аое]р|ик)|
    охую
  )|
  бля(?:[дбц]|тс)|
  [ое]ху[яйиеё]|
  хуйн
).*?|

(?:о[тб]?|про|на|вы)?м(?:
  анд(?:[ауеыи](?:л(?:и[сзщ])?[ауеиы])?|ой|[ао]в.*?|юк(?:ов|[ауи])?|е[нт]ь|ища)|
  уд(?:[яаиое].+?|е?н(?:[ьюия]|ей))|
  [ао]л[ао]ф[ьъ](?:[яиюе]|[еёо]й)
)|

елд[ауые].*?|
ля[тд]ь|
(?:[нз]а|по)х
)(?![а-яё])
"""


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self) -> NoReturn:
        if not self.value:
            raise EmptyTextException()

        if re.match(pattern.strip(), self.value):
            raise ObsceneTextException(self.value)

    def as_generic_type(self) -> str:
        return self.value


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self) -> NoReturn:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 30:
            raise TextTooLongException(self.value)

        if re.match(pattern.strip(), self.value):
            raise ObsceneTextException(self.value)

    def as_generic_type(self) -> str:
        return self.value
