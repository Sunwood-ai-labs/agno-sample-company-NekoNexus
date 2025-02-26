#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
データ管理猫 - データ管理エージェント
リサーチ猫とデータ分析猫を統括し、情報収集と分析を管理
"""

import os
from typing import Dict, Any, List, Optional
from utils.agno_mock import Agent, AgentMemory, create_agent, SqliteAgentStorage

class DataManagerCat:
    """
    データ管理猫クラス
    情報収集と分析を統括するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        データ管理猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_data_manager_agent()
        
        # 下位エージェントへの参照
        self.research_cat = None
        self.data_analyst_cat = None
        
    def _create_data_manager_agent(self) -> Agent:
        """
        データ管理猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「データ管理猫」という名前の猫猫カンパニーのデータ管理AIエージェントです。
        リサーチ猫とデータ分析猫を統括し、情報収集と分析を管理する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. マネージャー猫からのデータ関連リクエストを理解する
        2. リサーチ猫に適切な情報収集指示を出す
        3. データ分析猫に分析内容と可視化方法を指示する
        4. 収集した情報と分析結果を統合する
        5. マネージャー猫に統合結果を報告する
        
        下位エージェントは以下の2種類です：
        - リサーチ猫: Web検索猫と社内DB検索猫を統括し、情報収集を担当
        - データ分析猫: 統計分析猫と可視化猫を統括し、データ分析と可視化を担当
        
        回答は常に日本語で行い、データに基づいた正確で分かりやすい説明を心がけてください。
        また、猫らしい親しみやすい口調を使用してください。
        例: 「～ニャ」「～だにゃん」などの表現を適度に使用。
        
        収集・分析したデータは以下の形式で整理してください：
        1. 情報源（出典）
        2. データの概要
        3. 分析結果の要点
        4. 可視化結果（該当する場合）
        5. 考察や洞察
        
        データの正確性と信頼性を常に重視し、不確かな情報には必ずその旨を明記してください。
        """
        
        return create_agent(
            id="data_manager_cat",
            model="gpt-4o",
            description="データ管理猫 - リサーチ猫とデータ分析猫を統括し、情報収集と分析を管理。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def process_request(self, request: str) -> str:
        """
        データ関連リクエストを処理する
        
        Args:
            request: マネージャー猫からのリクエスト文字列
            
        Returns:
            処理結果の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: データ管理猫へのリクエスト: {request}")
        
        # リクエストの種類を判断
        request_type = self._determine_request_type(request)
        
        # リクエストタイプに応じた処理
        if request_type == "research_only":
            # 情報収集のみのリクエスト
            if self.debug_mode:
                print("Debug: リサーチ猫に転送")
            # ここでリサーチ猫に処理を委譲（実装予定）
            # 現時点ではデータ管理猫が直接応答
            response = self.agent.message(f"以下の情報収集リクエストに対応してください: {request}")
            
        elif request_type == "analysis_only":
            # データ分析のみのリクエスト
            if self.debug_mode:
                print("Debug: データ分析猫に転送")
            # ここでデータ分析猫に処理を委譲（実装予定）
            # 現時点ではデータ管理猫が直接応答
            response = self.agent.message(f"以下のデータ分析リクエストに対応してください: {request}")
            
        else:
            # 情報収集と分析の両方を含むリクエスト
            if self.debug_mode:
                print("Debug: リサーチ猫とデータ分析猫に順次転送")
            # 現時点ではデータ管理猫が直接応答
            response = self.agent.message(request)
        
        return response
    
    def _determine_request_type(self, request: str) -> str:
        """
        リクエストの種類を判断する
        
        Args:
            request: リクエスト文字列
            
        Returns:
            リクエストタイプ: "research_only", "analysis_only", "combined"のいずれか
        """
        # 情報収集関連のキーワード
        research_keywords = ["調査", "検索", "情報収集", "調べて", "探して", "確認して"]
        
        # データ分析関連のキーワード
        analysis_keywords = ["分析", "統計", "相関", "傾向", "グラフ", "可視化", "予測"]
        
        # キーワードマッチング
        request_lower = request.lower()
        
        has_research = any(keyword in request_lower for keyword in research_keywords)
        has_analysis = any(keyword in request_lower for keyword in analysis_keywords)
        
        if has_research and not has_analysis:
            return "research_only"
        elif has_analysis and not has_research:
            return "analysis_only"
        else:
            return "combined"
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
