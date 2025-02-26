"""
agnoパッケージのモック実装
実際のagnoパッケージがインストールされていない場合のスタブとして使用
"""

# モジュール構造を実際のagnoパッケージに合わせて調整
from .agent import Agent, AgentMemory, create_agent
from .storage import SqliteAgentStorage

# モックツールとモデルのクラス
from .tools import DuckDuckGoTools, YFinanceTools
from .models import OpenAIChat

# 列挙型
from enum import Enum
class SearchType(Enum):
    WEB = "web"
    NEWS = "news"
    IMAGES = "images"

__all__ = [
    "Agent", "AgentMemory", "create_agent", "SqliteAgentStorage",
    "OpenAIChat", "DuckDuckGoTools", "YFinanceTools", "SearchType"
]
