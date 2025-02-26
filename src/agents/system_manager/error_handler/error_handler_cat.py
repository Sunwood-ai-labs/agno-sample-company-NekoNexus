#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
エラー対応猫 - エラー対応エージェント
システムで発生したエラーの解析と対応を担当
"""

import os
import time
import platform
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Callable
from agno import Agent, AgentMemory, create_agent
from agno.storage import SqliteAgentStorage

class ErrorHandlerCat:
    """
    エラー対応猫クラス
    システムエラーの解析と対応を担当するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        エラー対応猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_error_handler_agent()
        
        # エラー履歴
        self.error_history = []
        self.max_history_length = 100
        
        # エラーログのパス
        self.error_log_path = os.path.join(os.getcwd(), "logs", "error.log")
        
        # ロギング設定
        self._setup_logging()
        
    def _create_error_handler_agent(self) -> Agent:
        """
        エラー対応猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「エラー対応猫」という名前の猫猫カンパニーのエラー対応AIエージェントです。
        システムに発生したエラーや問題を分析し、解決策を提案する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. システム管理猫からのエラー対応リクエストを理解する
        2. エラーログや例外情報を分析する
        3. エラーの原因を特定する
        4. 解決策や回避策を提案する
        5. 実施した対応策と結果を記録する
        6. システム管理猫に対応結果を報告する
        
        エラー対応の際は以下の点に注意してください：
        1. エラーの重要度と影響範囲を判断する
        2. エラーメッセージやスタックトレースから根本原因を分析する
        3. 既知の問題パターンと照合する
        4. 緊急度に応じた対応優先度を設定する
        5. 対応履歴を参照し、繰り返し発生するエラーを特定する
        
        回答は常に日本語で行い、技術的なエラー情報を分かりやすく説明してください。
        また、猫らしい冷静で解決志向な口調を使用してください。
        例: 「～が原因と思われるニャ」「～を試してみるにゃ」などの表現を適度に使用。
        
        エラー対応レポートは以下の形式で整理してください：
        1. エラー概要
        2. エラーの詳細分析
        3. 考えられる原因
        4. 推奨される対応策（優先順位付き）
        5. 予防策の提案
        
        常に冷静な分析を心がけ、最も効果的な解決策を提案してください。
        """
        
        return create_agent(
            id="error_handler_cat",
            model="gpt-4o",
            description="エラー対応猫 - システムエラーの解析と対応を担当する。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def _setup_logging(self):
        """
        ロギング設定を行う
        """
        # ログディレクトリの作成
        os.makedirs(os.path.dirname(self.error_log_path), exist_ok=True)
        
        # ロガーの設定
        self.logger = logging.getLogger("error_handler_cat")
        self.logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        
        # ファイルハンドラの設定
        file_handler = logging.FileHandler(self.error_log_path)
        file_handler.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        
        # フォーマッタの設定
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # ハンドラをロガーに追加
        self.logger.addHandler(file_handler)
        
        if self.debug_mode:
            print(f"Debug: エラーログファイルを設定しました: {self.error_log_path}")
    
    def handle_error(self, error_info: Dict[str, Any]) -> str:
        """
        エラー情報を処理し、対応策を提案する
        
        Args:
            error_info: エラー情報を含む辞書
                {
                    "type": エラータイプ,
                    "message": エラーメッセージ,
                    "traceback": スタックトレース,
                    "timestamp": エラー発生時刻,
                    "context": エラー発生コンテキスト
                }
            
        Returns:
            エラー対応結果のレポート
        """
        # エラーログに記録
        self._log_error(error_info)
        
        # エラー履歴に追加
        self._add_to_history(error_info)
        
        # エラー情報を整形
        error_desc = self._format_error_info(error_info)
        
        # 既知のエラーパターンと照合
        known_patterns = self._match_known_patterns(error_info)
        
        # エラー対応エージェントによる分析と対応提案
        request = f"""
        以下のエラー情報を分析し、対応策を提案してください。

        {error_desc}
        
        {'既知のエラーパターンと一致する可能性があります:' if known_patterns else '既知のエラーパターンとは一致しませんでした。'}
        {self._format_known_patterns(known_patterns) if known_patterns else ''}
        
        過去のエラー履歴:
        {self._get_similar_errors_summary(error_info)}
        """
        
        response = self.agent.message(request)
        
        # 対応結果をログに記録
        self._log_response(error_info, response)
        
        return response
    
    def _log_error(self, error_info: Dict[str, Any]):
        """
        エラー情報をログに記録する
        
        Args:
            error_info: エラー情報
        """
        error_msg = f"エラー検出: {error_info.get('type', 'Unknown')} - {error_info.get('message', 'No message')}"
        self.logger.error(error_msg)
        
        if 'traceback' in error_info and error_info['traceback']:
            self.logger.error(f"スタックトレース: {error_info['traceback']}")
        
        if 'context' in error_info and error_info['context']:
            self.logger.error(f"コンテキスト: {error_info['context']}")
    
    def _log_response(self, error_info: Dict[str, Any], response: str):
        """
        エラー対応結果をログに記録する
        
        Args:
            error_info: エラー情報
            response: エラー対応結果
        """
        error_type = error_info.get('type', 'Unknown')
        error_msg = error_info.get('message', 'No message')
        
        self.logger.info(f"エラー対応: {error_type} - {error_msg}")
        self.logger.info(f"対応結果: {response[:100]}...（省略）")
    
    def _add_to_history(self, error_info: Dict[str, Any]):
        """
        エラー情報を履歴に追加する
        
        Args:
            error_info: エラー情報
        """
        self.error_history.append(error_info)
        
        # 履歴サイズを制限
        if len(self.error_history) > self.max_history_length:
            self.error_history.pop(0)
    
    def _format_error_info(self, error_info: Dict[str, Any]) -> str:
        """
        エラー情報を読みやすい形式にフォーマットする
        
        Args:
            error_info: エラー情報
            
        Returns:
            フォーマットされたエラー情報
        """
        formatted = "エラー情報:\n"
        formatted += f"- タイプ: {error_info.get('type', 'Unknown')}\n"
        formatted += f"- メッセージ: {error_info.get('message', 'No message')}\n"
        
        if 'timestamp' in error_info:
            timestamp = error_info['timestamp']
            if isinstance(timestamp, (int, float)):
                timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            formatted += f"- 発生時刻: {timestamp}\n"
        
        if 'context' in error_info and error_info['context']:
            formatted += f"- コンテキスト: {error_info['context']}\n"
        
        if 'traceback' in error_info and error_info['traceback']:
            formatted += f"\nスタックトレース:\n{error_info['traceback']}\n"
        
        return formatted
    
    def _match_known_patterns(self, error_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        既知のエラーパターンと照合する
        
        Args:
            error_info: エラー情報
            
        Returns:
            一致した既知のエラーパターンリスト
        """
        # ここでは簡易的なパターンマッチングを実装
        # 実際のシステムではより高度なパターンマッチングが必要
        
        known_patterns = []
        
        # エラータイプによるマッチング
        error_type = error_info.get('type', '')
        error_msg = error_info.get('message', '')
        
        # メモリエラーパターン
        if "MemoryError" in error_type or "memory" in error_msg.lower():
            known_patterns.append({
                "pattern_id": "MEM001",
                "name": "メモリ不足エラー",
                "description": "プロセスがメモリ制限に達しました。",
                "solution": "メモリを増設するか、アプリケーションのメモリ使用量を最適化してください。",
                "confidence": 0.8 if "MemoryError" in error_type else 0.5
            })
        
        # データベース接続エラーパターン
        if "database" in error_msg.lower() or "sql" in error_msg.lower() or "connection" in error_msg.lower():
            known_patterns.append({
                "pattern_id": "DB001",
                "name": "データベース接続エラー",
                "description": "データベースへの接続が確立できないか、接続が切断されました。",
                "solution": "データベースサーバーの状態を確認し、接続設定を見直してください。",
                "confidence": 0.7 if "sql" in error_msg.lower() else 0.4
            })
        
        # ファイル操作エラーパターン
        if "FileNotFoundError" in error_type or "permission" in error_msg.lower() or "file" in error_msg.lower():
            known_patterns.append({
                "pattern_id": "FILE001",
                "name": "ファイル操作エラー",
                "description": "ファイルが見つからないか、アクセス権限がありません。",
                "solution": "ファイルの存在と権限を確認してください。",
                "confidence": 0.75 if "FileNotFoundError" in error_type else 0.5
            })
        
        # ネットワークエラーパターン
        if "ConnectionError" in error_type or "timeout" in error_msg.lower() or "network" in error_msg.lower():
            known_patterns.append({
                "pattern_id": "NET001",
                "name": "ネットワーク接続エラー",
                "description": "ネットワーク接続に問題があるか、リクエストがタイムアウトしました。",
                "solution": "ネットワーク接続を確認し、タイムアウト設定を調整してください。",
                "confidence": 0.7 if "ConnectionError" in error_type else 0.5
            })
        
        return known_patterns
    
    def _format_known_patterns(self, patterns: List[Dict[str, Any]]) -> str:
        """
        既知のエラーパターン情報をフォーマットする
        
        Args:
            patterns: エラーパターンリスト
            
        Returns:
            フォーマットされたパターン情報
        """
        if not patterns:
            return "一致するパターンはありません。"
        
        formatted = ""
        for pattern in patterns:
            confidence = pattern.get('confidence', 0) * 100
            formatted += f"パターンID: {pattern.get('pattern_id', 'Unknown')}"
            formatted += f" (一致度: {confidence:.0f}%)\n"
            formatted += f"- 名前: {pattern.get('name', 'Unknown')}\n"
            formatted += f"- 説明: {pattern.get('description', 'No description')}\n"
            formatted += f"- 推奨対応: {pattern.get('solution', 'No solution')}\n\n"
        
        return formatted
    
    def _get_similar_errors_summary(self, current_error: Dict[str, Any]) -> str:
        """
        過去に発生した類似エラーの要約を取得する
        
        Args:
            current_error: 現在のエラー情報
            
        Returns:
            類似エラーの要約
        """
        similar_errors = []
        
        # 簡易的な類似度計算
        # 実際のシステムではより高度な類似度計算が必要
        for error in self.error_history:
            if error is current_error:
                continue
                
            similarity_score = 0
            
            # エラータイプの一致
            if error.get('type') == current_error.get('type'):
                similarity_score += 0.5
            
            # メッセージの部分一致
            if error.get('message') and current_error.get('message'):
                if error.get('message') in current_error.get('message') or \
                   current_error.get('message') in error.get('message'):
                    similarity_score += 0.3
            
            # コンテキストの一致
            if error.get('context') == current_error.get('context'):
                similarity_score += 0.2
            
            if similarity_score > 0.5:
                similar_errors.append((error, similarity_score))
        
        # スコア順にソート
        similar_errors.sort(key=lambda x: x[1], reverse=True)
        
        # 上位3件までを使用
        similar_errors = similar_errors[:3]
        
        if not similar_errors:
            return "過去に類似したエラーは見つかりませんでした。"
        
        formatted = ""
        for i, (error, score) in enumerate(similar_errors):
            similarity_percent = score * 100
            timestamp = error.get('timestamp', 'Unknown time')
            if isinstance(timestamp, (int, float)):
                timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            formatted += f"{i+1}. エラータイプ: {error.get('type', 'Unknown')}\n"
            formatted += f"   メッセージ: {error.get('message', 'No message')[:50]}...\n"
            formatted += f"   発生時刻: {timestamp}\n"
            formatted += f"   類似度: {similarity_percent:.0f}%\n\n"
        
        return formatted
