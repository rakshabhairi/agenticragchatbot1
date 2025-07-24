# mcp/message_dispatcher.py

class MCPMessage:
    def __init__(self, sender, receiver, type, payload, trace_id=None):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.payload = payload
        self.trace_id = trace_id


class MCPDispatcher:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name, handler):
        self.agents[name] = handler

    def send_message(self, message: MCPMessage):
        receiver_handler = self.agents.get(message.receiver)
        if not receiver_handler:
            raise ValueError(f"No handler registered for {message.receiver}")
        return receiver_handler(message)
