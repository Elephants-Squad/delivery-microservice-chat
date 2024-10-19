from fastapi import Depends, Request
from typing import Type, TypeVar, Callable, Any

T = TypeVar('T')


def Service(service_type: Type[T]) -> Any: # noqa: N802
    def resolve_service(request: Request) -> Callable[[], T]:
        return request.app.state.ioc_container.resolve(service_type)
    return Depends(resolve_service)
