from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from typing import Type

from app.domain.events.base import BaseEvent
from app.logic.commands.base import CR, CT, BaseCommand, CommandHandler
from app.logic.events.base import ER, ET, EventHandler
from app.logic.exceptions.mediator import CommandHandlersNotRegisteredException


@dataclass(eq=False)
class Mediator:
    events_map: dict[Type[ET], list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[Type[CT], list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_event(self, event: Type[ET], event_handlers: Iterable[EventHandler[ET, ER]]) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(self, command: Type[CT], command_handlers: Iterable[CommandHandler[CT, CR]]) -> None:
        self.commands_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[Type[BaseEvent]]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers = self.events_map[event]
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]