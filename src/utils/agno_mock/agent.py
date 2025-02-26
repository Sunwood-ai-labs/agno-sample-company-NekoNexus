"""
agnoパッケージのAgent関連クラスのモック実装
"""

from typing import Dict, Any, List, Optional, Union, Callable
import uuid
import json
import time

class AgentMemory:
    """
    エージェントメモリのモッククラス
    """
    
    def __init__(self):
        """
        メモリの初期化
        """
        self._memories = {}
        
    def add(self, key: str, value: Any):
        """
        メモリにキーと値を追加
        
        Args:
            key: 記憶のキー
            value: 記憶の値
        """
        self._memories[key] = value
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        メモリからキーに紐づく値を取得
        
        Args:
            key: 取得する記憶のキー
            default: キーが存在しない場合のデフォルト値
            
        Returns:
            記憶の値またはデフォルト値
        """
        return self._memories.get(key, default)
        
    def remove(self, key: str):
        """
        メモリから記憶を削除
        
        Args:
            key: 削除する記憶のキー
        """
        if key in self._memories:
            del self._memories[key]
            
    def clear(self):
        """
        メモリをクリア
        """
        self._memories.clear()
        
    def keys(self) -> List[str]:
        """
        メモリ内のすべてのキーを取得
        
        Returns:
            キーのリスト
        """
        return list(self._memories.keys())
        
    def items(self) -> Dict[str, Any]:
        """
        メモリ内のすべてのキーと値のペアを取得
        
        Returns:
            キーと値の辞書
        """
        return self._memories.copy()


class Agent:
    """
    エージェントのモッククラス
    """
    
    def __init__(self, id: str, model: str, description: str, instructions: str, 
                 memory: Optional[AgentMemory] = None, storage = None, 
                 markdown: bool = True, show_tool_calls: bool = False, 
                 add_history_to_messages: bool = True):
        """
        エージェントの初期化
        
        Args:
            id: エージェントID
            model: 使用するモデル名
            description: エージェントの説明
            instructions: エージェントの指示
            memory: エージェントメモリ
            storage: エージェントストレージ
            markdown: マークダウン形式を使用するかどうか
            show_tool_calls: ツール呼び出しを表示するかどうか
            add_history_to_messages: メッセージ履歴を追加するかどうか
        """
        self.id = id
        self.model = model
        self.description = description
        self.instructions = instructions
        self.memory = memory or AgentMemory()
        self.storage = storage
        self.markdown = markdown
        self.show_tool_calls = show_tool_calls
        self.add_history_to_messages = add_history_to_messages
        
        # メッセージ履歴
        self.message_history = []
        
    def message(self, content: str) -> str:
        """
        エージェントにメッセージを送信し、応答を取得
        
        Args:
            content: メッセージ内容
            
        Returns:
            エージェントからの応答
        """
        # 実際のAIモデル呼び出しの代わりにモック応答を生成
        message_id = str(uuid.uuid4())
        timestamp = time.time()
        
        # メッセージをヒストリーに追加
        self.message_history.append({
            "id": message_id,
            "role": "user",
            "content": content,
            "timestamp": timestamp
        })
        
        # モック応答の生成
        response = self._generate_mock_response(content)
        
        # 応答をヒストリーに追加
        self.message_history.append({
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": response,
            "timestamp": time.time()
        })
        
        return response
        
    def _generate_mock_response(self, content: str) -> str:
        """
        モック応答を生成
        
        Args:
            content: 入力メッセージ
            
        Returns:
            モック応答
        """
        # この実装は本番では実際のAIモデルに置き換える
        agent_type = "不明"
        if "マネージャー猫" in self.description:
            agent_type = "マネージャー猫"
        elif "データ管理猫" in self.description:
            agent_type = "データ管理猫"
        elif "リサーチ猫" in self.description:
            agent_type = "リサーチ猫"
        elif "データ分析猫" in self.description:
            # データ分析猫の場合、特別な応答を生成（実際の分析機能を模擬）
            agent_type = "データ分析猫"
            if "売上" in content and "分析" in content:
                return f"""# 📊 データ分析結果

売上データの分析を行いましたにゃ～。詳しい分析はマネージャー猫から受け取ったデータを使って実施しています。
グラフとともに詳細な分析結果をご確認くださいにゃ！

## 分析ポイント
- 売上傾向
- 商品別の販売状況
- 顧客数との相関関係

どの商品が一番売れているか、どの日の売上が最も高かったかなどを確認できますにゃ。
ご質問があればお気軽にどうぞ～（=^・ω・^=）"""
            else:
                return f"""# 📈 データ分析レポート

ご依頼の分析を行いましたにゃ！

{content}というリクエストについて、分析を実施しましたが、詳細なデータが必要です。
どのようなデータを分析すればよいか、より詳しく教えていただけますか？

データ分析猫より（=^・ω・^=）"""
        elif "業務遂行猫" in self.description:
            agent_type = "業務遂行猫"
        elif "ドキュメント猫" in self.description:
            agent_type = "ドキュメント猫"
        elif "スケジュール猫" in self.description:
            agent_type = "スケジュール猫"
        elif "システム管理猫" in self.description:
            agent_type = "システム管理猫"
        elif "監視猫" in self.description:
            agent_type = "監視猫"
        elif "エラー対応猫" in self.description:
            agent_type = "エラー対応猫"
            
        return f"""# 🐾 {agent_type}からの応答

{content}について調査しました。

詳細情報は現在準備中ですにゃ～。もう少し具体的なリクエストをいただけると助かりますにゃ！

何かご質問があれば、お気軽にどうぞ（=^・ω・^=）"""
        
def create_agent(id: str, model: str, description: str, instructions: str, 
                 memory: Optional[AgentMemory] = None, storage = None, 
                 markdown: bool = True, show_tool_calls: bool = False, 
                 add_history_to_messages: bool = True) -> Agent:
    """
    新しいエージェントを作成するヘルパー関数
    
    Args:
        id: エージェントID
        model: 使用するモデル名
        description: エージェントの説明
        instructions: エージェントの指示
        memory: エージェントメモリ
        storage: エージェントストレージ
        markdown: マークダウン形式を使用するかどうか
        show_tool_calls: ツール呼び出しを表示するかどうか
        add_history_to_messages: メッセージ履歴を追加するかどうか
        
    Returns:
        作成されたエージェントインスタンス
    """
    return Agent(
        id=id,
        model=model,
        description=description,
        instructions=instructions,
        memory=memory,
        storage=storage,
        markdown=markdown,
        show_tool_calls=show_tool_calls,
        add_history_to_messages=add_history_to_messages
    )
