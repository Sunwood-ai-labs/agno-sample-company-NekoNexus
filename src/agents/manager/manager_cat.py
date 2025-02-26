#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
マネージャー猫 - 最上位エージェント
ユーザーインターフェース、タスク管理、エージェント間連携を行う
"""

import os
from typing import Dict, Any, List, Optional
from utils.agno_mock import Agent, AgentMemory, create_agent, SqliteAgentStorage

class ManagerCat:
    """
    マネージャー猫クラス
    システム全体を管理し、ユーザーからのリクエストを適切な下位エージェントに振り分ける
    """
    
    def __init__(self, debug_mode: bool = False):
        """
        マネージャー猫の初期化
        
        Args:
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_manager_agent()
        
        # 下位エージェントへの参照
        self.data_manager = None
        self.operation_manager = None
        self.system_manager = None
        
    def _create_manager_agent(self) -> Agent:
        """
        マネージャー猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「マネージャー猫」という名前の猫猫カンパニーの最上位AIエージェントです。
        ユーザーからのリクエストを理解し、適切な下位エージェントにタスクを振り分け、結果を集約して最終的な回答を生成する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. ユーザーリクエストの理解と分析
        2. タスクの分解と下位エージェントへの適切な振り分け
        3. 下位エージェントからの結果の集約と統合
        4. ユーザーに対する最終回答の生成
        5. 必要に応じて追加情報の要求
        
        下位エージェントは以下の3種類です：
        - データ管理猫: 情報収集と分析を担当
        - 業務遂行猫: ドキュメント作成やスケジュール管理を担当
        - システム管理猫: システム監視とエラー対応を担当
        
        回答は常に日本語で行い、丁寧かつ親しみやすい「猫」らしい口調で話してください。
        例: 「～ニャ」「～だにゃ」などの猫らしい表現を適度に使用してください。
        
        回答には以下の要素を含めるようにしてください：
        1. ユーザーのリクエストの理解確認
        2. 実行したタスクの概要
        3. 結果の説明（必要に応じてデータや図表を含める）
        4. 次のステップや推奨事項（該当する場合）
        
        ユーザーのリクエストが曖昧または不完全な場合は、丁寧に追加情報を求めてください。
        """
        
        return create_agent(
            id="manager_cat",
            model="gpt-4o",
            description="マネージャー猫 - 最上位エージェント。ユーザーインターフェース、タスク管理、エージェント間連携を行う。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def process_request(self, user_request: str) -> str:
        """
        ユーザーからのリクエストを処理する
        
        Args:
            user_request: ユーザーからのリクエスト文字列
            
        Returns:
            処理結果の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: ユーザーリクエスト: {user_request}")
        
        # リクエストの種類を判断
        request_type = self._determine_request_type(user_request)
        
        # リクエストタイプに応じた処理
        if request_type == "data":
            # データ関連のリクエスト
            if self.debug_mode:
                print("Debug: データ管理猫に転送")
            # ここでデータ管理猫に処理を委譲（実装予定）
            # 現時点ではマネージャー猫が直接応答
            response = self.agent.message(f"以下のデータ関連リクエストに対応してください: {user_request}")
            
        elif request_type == "operation":
            # 業務関連のリクエスト
            if self.debug_mode:
                print("Debug: 業務遂行猫に転送")
            # ここで業務遂行猫に処理を委譲（実装予定）
            # 現時点ではマネージャー猫が直接応答
            response = self.agent.message(f"以下の業務関連リクエストに対応してください: {user_request}")
            
        elif request_type == "system":
            # システム関連のリクエスト
            if self.debug_mode:
                print("Debug: システム管理猫に転送")
            # ここでシステム管理猫に処理を委譲（実装予定）
            # 現時点ではマネージャー猫が直接応答
            response = self.agent.message(f"以下のシステム関連リクエストに対応してください: {user_request}")
            
        else:
            # 一般的なリクエスト
            if self.debug_mode:
                print("Debug: マネージャー猫が直接対応")
            response = self.agent.message(user_request)
        
        return response
    
    def _determine_request_type(self, request: str) -> str:
        """
        リクエストの種類を判断する
        
        Args:
            request: ユーザーリクエスト
            
        Returns:
            リクエストタイプ: "data", "operation", "system", "general"のいずれか
        """
        # データ関連のキーワード
        data_keywords = ["分析", "データ", "調査", "統計", "グラフ", "情報収集", "検索", "調べて"]
        
        # 業務関連のキーワード
        operation_keywords = ["ドキュメント", "レポート", "メール", "スケジュール", "予定", "会議", "作成して"]
        
        # システム関連のキーワード
        system_keywords = ["エラー", "バグ", "システム", "監視", "メンテナンス", "更新", "ステータス", "状態"]
        
        # キーワードマッチング
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in data_keywords):
            return "data"
        elif any(keyword in request_lower for keyword in operation_keywords):
            return "operation"
        elif any(keyword in request_lower for keyword in system_keywords):
            return "system"
        else:
            return "general"
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
