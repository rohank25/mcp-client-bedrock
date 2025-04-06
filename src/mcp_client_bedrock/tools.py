from pydantic import BaseModel, Field, PrivateAttr
from typing import Dict, Callable, List

class BedrockToolManager(BaseModel):
    tools: Dict = Field(default_factory=dict)
    _name_mapping: Dict = PrivateAttr(default_factory=dict)

    # Converse API requirement
    def _sanitize_name(self, name: str) -> str:
        return name.replace('-', '_')
    
    def add_tool(self, name: str, desc: str, schema: Dict) -> None:
        if not self.tools:
            self.tools['tools'] = []
        sanitized_name = self._sanitize_name(name)
        self._name_mapping[sanitized_name] = name
        self.tools['tools'].append({
            'toolSpec': {
                'name': sanitized_name,
                'description': desc,
                'inputSchema': schema
            },
        })
