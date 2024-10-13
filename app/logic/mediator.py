from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from app.domain.events.base import BaseEvent
from app.logic.commands.base import CR, CT, BaseCommand, CommandHandler
from app.logic.events.base import ER, ET, EventHandler
from app.logic.exceptions.mediator import CommandHandlersNotRegisteredException


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]) -> None:
        self.commands_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[event]
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        handlers = self.commands_map.get(command)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command.__class__)

        return [await handler.handle(command) for handler in handlers]