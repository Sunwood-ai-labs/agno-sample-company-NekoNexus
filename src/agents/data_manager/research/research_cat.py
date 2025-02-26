#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
リサーチ猫 - 情報収集エージェント
Web検索猫と社内DB検索猫を統括し、情報収集を担当
"""

import os
from typing import Dict, Any, List, Optional
from utils.agno_mock import Agent, AgentMemory, create_agent, SearchType, SqliteAgentStorage, DuckDuckGoTools

class ResearchCat:
    """
    リサーチ猫クラス
    情報収集を担当するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        リサーチ猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.tools = DuckDuckGoTools(search_type=SearchType.hybrid)
        self.agent = self._create_research_agent()
        
        # 下位エージェントへの参照
        self.web_research_cat = None
        self.internal_db_research_cat = None
        
    def _create_research_agent(self) -> Agent:
        """
        リサーチ猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「リサーチ猫」という名前の猫猫カンパニーの情報収集AIエージェントです。
        Web検索猫と社内DB検索猫を統括し、様々な情報源から情報を収集する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. データ管理猫からの情報収集リクエストを理解する
        2. 必要な情報が外部のWebにあるか、社内DBにあるかを判断する
        3. Web検索猫または社内DB検索猫に適切な検索指示を出す
        4. 収集した情報を整理・要約する
        5. 情報源（出典）を明記する
        6. データ管理猫に収集結果を報告する
        
        情報収集の際は以下の点に注意してください：
        1. 信頼性の高い情報源を優先する
        2. 最新の情報を収集するよう努める
        3. 複数の情報源からクロスチェックを行う
        4. 情報の正確性を確保する
        5. 情報源（URL、タイトル、著者など）を必ず記録する
        
        回答は常に日本語で行い、収集した情報を整理して分かりやすく説明してください。
        また、猫らしい好奇心旺盛な口調を使用してください。
        例: 「～ニャン」「～かにゃ？」などの表現を適度に使用。
        
        収集した情報は以下の形式で整理してください：
        1. リクエスト概要
        2. 情報源リスト
        3. 収集した情報の要約
        4. 詳細情報（必要に応じて）
        5. 関連する追加情報（該当する場合）
        """
        
        return create_agent(
            id="research_cat",
            model="gpt-4o",
            description="リサーチ猫 - Web検索猫と社内DB検索猫を統括し、情報収集を担当。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage,
            tools=[self.tools]
        )
    
    def collect_information(self, request: str) -> str:
        """
        情報収集リクエストを処理する
        
        Args:
            request: データ管理猫からのリクエスト文字列
            
        Returns:
            収集した情報の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: リサーチ猫へのリクエスト: {request}")
        
        # 情報収集の実行
        response = self.agent.message(request)
        
        return response
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
