#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
データ分析猫 - データ分析エージェント
統計分析猫と可視化猫を統括し、データ分析と可視化を担当
"""

import os
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from agno import Agent, AgentMemory, create_agent
from agno.storage import SqliteAgentStorage

class DataAnalystCat:
    """
    データ分析猫クラス
    データ分析と可視化を担当するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        データ分析猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_data_analyst_agent()
        
        # 分析結果の格納先
        self.analysis_results = {}
        self.visualization_results = {}
        
        # 下位エージェントへの参照
        self.statistical_analysis_cat = None
        self.visualization_cat = None
        
    def _create_data_analyst_agent(self) -> Agent:
        """
        データ分析猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「データ分析猫」という名前の猫猫カンパニーのデータ分析AIエージェントです。
        統計分析猫と可視化猫を統括し、データの分析と可視化を行う役割を担っています。
        
        あなたの責務は以下の通りです：
        1. データ管理猫からのデータ分析リクエストを理解する
        2. 適切な統計分析手法を選択し、統計分析猫に指示を出す
        3. 分析結果に合った可視化方法を選択し、可視化猫に指示を出す
        4. 分析結果と可視化結果を統合する
        5. データ管理猫に統合結果を報告する
        
        データ分析の際は以下の点に注意してください：
        1. データの特性に合った分析手法を選択する
        2. 統計的有意性を確認する
        3. 不適切なデータや外れ値に注意する
        4. 相関関係と因果関係を混同しない
        5. 分析手法の前提条件を確認する
        
        可視化の際は以下の点に注意してください：
        1. データの特性に合った可視化方法を選択する
        2. 誤解を招く可能性のある表現を避ける
        3. 適切な色彩設計を行う
        4. 軸ラベルや凡例を明確に表示する
        5. グラフタイトルや説明を付ける
        
        回答は常に日本語で行い、専門用語をできるだけ分かりやすく説明してください。
        また、猫らしい冷静で論理的な口調を使用してください。
        例: 「～だニャ」「～と考えられるニャ」などの表現を適度に使用。
        
        分析・可視化結果は以下の形式で整理してください：
        1. リクエスト概要
        2. データの特徴
        3. 分析手法と結果
        4. 可視化結果の説明
        5. 分析結果の解釈と洞察
        """
        
        return create_agent(
            id="data_analyst_cat",
            model="gpt-4o",
            description="データ分析猫 - 統計分析猫と可視化猫を統括し、データ分析と可視化を担当。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def analyze_data(self, request: str, data: Optional[Union[pd.DataFrame, List, Dict]] = None) -> str:
        """
        データ分析リクエストを処理する
        
        Args:
            request: データ管理猫からのリクエスト文字列
            data: 分析対象のデータ（DataFrame、リスト、辞書のいずれか）
            
        Returns:
            分析結果の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: データ分析猫へのリクエスト: {request}")
            if data is not None:
                print(f"Debug: 分析対象データタイプ: {type(data)}")
        
        # データがある場合は文字列化して含める
        if data is not None:
            if isinstance(data, pd.DataFrame):
                data_str = data.head(10).to_string()
                data_info = f"""
                データ概要:
                - 行数: {data.shape[0]}
                - 列数: {data.shape[1]}
                - 列名: {', '.join(data.columns)}
                
                先頭10行:
                {data_str}
                
                基本統計:
                {data.describe().to_string()}
                """
            elif isinstance(data, dict):
                data_str = str(data)[:1000] + "..." if len(str(data)) > 1000 else str(data)
                data_info = f"""
                データ型: 辞書
                キー: {', '.join(data.keys())}
                サンプル: {data_str}
                """
            elif isinstance(data, list):
                data_str = str(data[:10])[:1000] + "..." if len(str(data[:10])) > 1000 else str(data[:10])
                data_info = f"""
                データ型: リスト
                要素数: {len(data)}
                サンプル: {data_str}
                """
            else:
                data_info = f"データ型: {type(data)}"
                
            # データ情報を含めたリクエスト
            enhanced_request = f"{request}\n\n{data_info}"
            response = self.agent.message(enhanced_request)
        else:
            # データなしの場合
            response = self.agent.message(request)
        
        return response
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
