from protester.event import subscribe


def handle_log_event(data):
    print(f"{data}")

class Variants_event_listener:
    def __init__(self) -> None:
        self.variants = []

    def handle_variants_event(self, variants):
        # store the event for later use
        self.variants = variants

    def get_variants(self):
        return self.variants

variant_event = Variants_event_listener()

def setup_log_event_handlers():
    subscribe("protester_log", handle_log_event)
    subscribe("test_variants", variant_event.handle_variants_event)