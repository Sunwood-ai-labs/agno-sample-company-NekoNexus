"""
agnoパッケージのストレージ関連クラスのモック実装
"""

import os
import json
import sqlite3
from typing import Dict, Any, List, Optional, Union, Callable
import uuid
import time

class SqliteAgentStorage:
    """
    SQLiteベースのエージェントストレージのモッククラス
    """
    
    def __init__(self, db_path: str):
        """
        ストレージの初期化
        
        Args:
            db_path: SQLiteデータベースファイルのパス
        """
        self.db_path = db_path
        self._ensure_database()
        
    def _ensure_database(self):
        """
        データベースとテーブルの存在を確認し、必要に応じて作成
        """
        # データベースディレクトリの作成
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        
        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # テーブル作成
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp REAL NOT NULL,
            metadata TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            timestamp REAL NOT NULL,
            metadata TEXT
        )
        ''')
        
        # インデックス作成
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_agent_id ON messages (agent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_agent_id ON memories (agent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_key ON memories (key)')
        
        conn.commit()
        conn.close()
        
    def save_message(self, agent_id: str, message: Dict[str, Any]) -> str:
        """
        エージェントのメッセージを保存
        
        Args:
            agent_id: エージェントID
            message: メッセージ辞書
            
        Returns:
            メッセージID
        """
        # メッセージIDがない場合は生成
        message_id = message.get('id', str(uuid.uuid4()))
        
        # タイムスタンプがない場合は現在時刻を設定
        timestamp = message.get('timestamp', time.time())
        
        # メタデータの処理
        metadata = message.get('metadata', {})
        if isinstance(metadata, dict):
            metadata = json.dumps(metadata)
        
        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # メッセージの保存
        cursor.execute(
            'INSERT OR REPLACE INTO messages (id, agent_id, role, content, timestamp, metadata) VALUES (?, ?, ?, ?, ?, ?)',
            (message_id, agent_id, message.get('role', 'user'), message.get('content', ''), timestamp, metadata)
        )
        
        conn.commit()
        conn.close()
        
        return message_id
        
    def get_messages(self, agent_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        エージェントのメッセージを取得
        
        Args:
            agent_id: エージェントID
            limit: 取得するメッセージの最大数
            offset: 取得開始位置のオフセット
            
        Returns:
            メッセージリスト
        """
        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # メッセージの取得
        cursor.execute(
            'SELECT id, role, content, timestamp, metadata FROM messages WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?',
            (agent_id, limit, offset)
        )
        
        messages = []
        for row in cursor.fetchall():
            message_id, role, content, timestamp, metadata = row
            
            # メタデータの処理
            try:
                metadata_dict = json.loads(metadata) if metadata else {}
            except json.JSONDecodeError:
                metadata_dict = {}
            
            messages.append({
                'id': message_id,
                'role': role,
                'content': content,
                'timestamp': timestamp,
                'metadata': metadata_dict
            })
        
        conn.close()
        
        # 時間順にソート
        messages.sort(key=lambda x: x['timestamp'])
        
        return messages
        
    def save_memory(self, agent_id: str, key: str, value: Any, metadata: Dict[str, Any] = None) -> str:
        """
        エージェントのメモリを保存
        
        Args:
            agent_id: エージェントID
            key: メモリキー
            value: メモリ値
            metadata: メタデータ
            
        Returns:
            メモリID
        """
        # メモリIDの生成
        memory_id = str(uuid.uuid4())
        
        # 値のJSON変換
        if not isinstance(value, str):
            value = json.dumps(value)
        
        # メタデータの処理
        if metadata is None:
            metadata = {}
        metadata_str = json.dumps(metadata)
        
        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # メモリの保存
        cursor.execute(
            'INSERT OR REPLACE INTO memories (id, agent_id, key, value, timestamp, metadata) VALUES (?, ?, ?, ?, ?, ?)',
            (memory_id, agent_id, key, value, time.time(), metadata_str)
        )
        
        conn.commit()
        conn.close()
        
        return memory_id
        
    def get_memory(self, agent_id: str, key: str) -> Optional[Any]:
        """
        エージェントのメモリを取得
        
        Args:
            agent_id: エージェントID
            key: メモリキー
            
        Returns:
            メモリ値（存在しない場合はNone）
        """
        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # メモリの取得
        cursor.execute(
            'SELECT value FROM memories WHERE agent_id = ? AND key = ? ORDER BY timestamp DESC LIMIT 1',
            (agent_id, key)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        value = row[0]
        
        # JSON値の復元を試みる
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
            
    def delete_memory(self, agent_id: str, key: str) -> bool:
        """
        エージェントのメモリを削除
        
        Args:
            agent_id: エージェントID
            key: メモリキー
            
        Returns:
            削除成功かどうか
        """
        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # メモリの削除
        cursor.execute(
            'DELETE FROM memories WHERE agent_id = ? AND key = ?',
            (agent_id, key)
        )
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected > 0
        
    def list_memories(self, agent_id: str) -> Dict[str, Any]:
        """
        エージェントのすべてのメモリを取得
        
        Args:
            agent_id: エージェントID
            
        Returns:
            キーと値のペアの辞書
        """
        # データベース接続
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ユニークなキーの取得
        cursor.execute(
            'SELECT DISTINCT key FROM memories WHERE agent_id = ?',
            (agent_id,)
        )
        
        keys = [row[0] for row in cursor.fetchall()]
        
        # 各キーの最新の値を取得
        memories = {}
        for key in keys:
            cursor.execute(
                'SELECT value FROM memories WHERE agent_id = ? AND key = ? ORDER BY timestamp DESC LIMIT 1',
                (agent_id, key)
            )
            row = cursor.fetchone()
            if row:
                value = row[0]
                # JSON値の復元を試みる
                try:
                    memories[key] = json.loads(value)
                except json.JSONDecodeError:
                    memories[key] = value
        
        conn.close()
        
        return memories
