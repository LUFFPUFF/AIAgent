from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any]

@dataclass
class Message:
    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str
    tool_calls: Optional[List[ToolCall]] = None

@dataclass
class ChatContext:
    messages: List[Message] = field(default_factory=list)

    def add_message(self, role: str, content: str, tool_calls: Optional[List[ToolCall]] = None):
        self.messages.append(Message(role=role, content=content, tool_calls=tool_calls))