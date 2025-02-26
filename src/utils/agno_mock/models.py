"""
agnoパッケージのモデルモックの実装
"""

class OpenAIChat:
    """
    OpenAI Chatモデルのモッククラス
    """
    
    def __init__(self, id="gpt-4o", temperature=0.7, max_tokens=None):
        """
        OpenAI Chatモデルの初期化
        
        Args:
            id: モデルID
            temperature: 温度パラメータ
            max_tokens: 最大トークン数
        """
        self.id = id
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def generate(self, messages, stream=False):
        """
        テキスト生成を行うモック関数
        
        Args:
            messages: メッセージリスト
            stream: ストリーミング生成を行うかどうか
            
        Returns:
            生成されたテキスト
        """
        # 実際にはAPIを呼び出さず、モック応答を返す
        last_message = messages[-1]["content"] if messages and "content" in messages[-1] else ""
        return f"これはOpenAI Chat ({self.id})からのモック応答です。\n\n入力メッセージ: {last_message[:50]}..."
