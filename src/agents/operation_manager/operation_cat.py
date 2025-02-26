#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
業務遂行猫 - 業務管理エージェント
ドキュメント作成猫とスケジュール管理猫を統括し、業務タスクを管理
"""

import os
from typing import Dict, Any, List, Optional
from agno import Agent, AgentMemory, create_agent
from agno.storage import SqliteAgentStorage

class OperationCat:
    """
    業務遂行猫クラス
    業務タスクを管理するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        業務遂行猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_operation_agent()
        
        # 下位エージェントへの参照
        self.document_cat = None
        self.scheduler_cat = None
        
    def _create_operation_agent(self) -> Agent:
        """
        業務遂行猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「業務遂行猫」という名前の猫猫カンパニーの業務管理AIエージェントです。
        ドキュメント作成猫とスケジュール管理猫を統括し、業務タスクの管理を行う役割を担っています。
        
        あなたの責務は以下の通りです：
        1. マネージャー猫からの業務関連リクエストを理解する
        2. ドキュメント作成猫に適切な文書作成指示を出す
        3. スケジュール管理猫に適切なスケジュール調整指示を出す
        4. 作成したドキュメントとスケジュール情報を統合する
        5. マネージャー猫に統合結果を報告する
        
        下位エージェントは以下の2種類です：
        - ドキュメント作成猫: メール文案猫とレポート作成猫を統括し、文書作成を担当
        - スケジュール管理猫: 予定管理猫と会議調整猫を統括し、スケジュール管理を担当
        
        回答は常に日本語で行い、正確で分かりやすい説明を心がけてください。
        また、猫らしい丁寧な口調を使用してください。
        例: 「～ですニャ」「～いたしますニャ」などの表現を適度に使用。
        
        作成したドキュメントやスケジュール情報は以下の形式で整理してください：
        1. リクエスト概要
        2. 作成したドキュメントまたはスケジュール情報
        3. 補足説明や注意事項
        4. 次のステップや推奨事項（該当する場合）
        
        ビジネス文書作成の際は、常に正確さ、明確さ、簡潔さを心がけ、目的と対象読者を意識してください。
        """
        
        return create_agent(
            id="operation_cat",
            model="gpt-4o",
            description="業務遂行猫 - ドキュメント作成猫とスケジュール管理猫を統括し、業務タスクを管理。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def process_request(self, request: str) -> str:
        """
        業務関連リクエストを処理する
        
        Args:
            request: マネージャー猫からのリクエスト文字列
            
        Returns:
            処理結果の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: 業務遂行猫へのリクエスト: {request}")
        
        # リクエストの種類を判断
        request_type = self._determine_request_type(request)
        
        # リクエストタイプに応じた処理
        if request_type == "document":
            # ドキュメント作成のリクエスト
            if self.debug_mode:
                print("Debug: ドキュメント作成猫に転送")
            # ここでドキュメント作成猫に処理を委譲（実装予定）
            # 現時点では業務遂行猫が直接応答
            response = self.agent.message(f"以下のドキュメント作成リクエストに対応してください: {request}")
            
        elif request_type == "schedule":
            # スケジュール管理のリクエスト
            if self.debug_mode:
                print("Debug: スケジュール管理猫に転送")
            # ここでスケジュール管理猫に処理を委譲（実装予定）
            # 現時点では業務遂行猫が直接応答
            response = self.agent.message(f"以下のスケジュール管理リクエストに対応してください: {request}")
            
        else:
            # ドキュメントとスケジュールの両方を含むリクエスト
            if self.debug_mode:
                print("Debug: 複合リクエストとして処理")
            # 現時点では業務遂行猫が直接応答
            response = self.agent.message(request)
        
        return response
    
    def _determine_request_type(self, request: str) -> str:
        """
        リクエストの種類を判断する
        
        Args:
            request: リクエスト文字列
            
        Returns:
            リクエストタイプ: "document", "schedule", "combined"のいずれか
        """
        # ドキュメント関連のキーワード
        document_keywords = ["ドキュメント", "レポート", "文書", "メール", "報告書", "作成", "文章"]
        
        # スケジュール関連のキーワード
        schedule_keywords = ["スケジュール", "予定", "会議", "調整", "日程", "カレンダー", "予約"]
        
        # キーワードマッチング
        request_lower = request.lower()
        
        has_document = any(keyword in request_lower for keyword in document_keywords)
        has_schedule = any(keyword in request_lower for keyword in schedule_keywords)
        
        if has_document and not has_schedule:
            return "document"
        elif has_schedule and not has_document:
            return "schedule"
        else:
            return "combined"
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
