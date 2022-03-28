from app.logic.events import Event


def handle(event: Event):
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in event.handlers:
            new_events, errors = handler(event)
            if errors:
                # если произошла ошибка, последующие события не выполняются,
                # выполняются только возникшие во время упавшего события
                queue = new_events
                break
            queue.extend(new_events)
