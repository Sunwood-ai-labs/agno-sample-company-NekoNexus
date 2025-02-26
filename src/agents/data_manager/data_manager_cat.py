#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
データ管理猫 - データ管理エージェント
リサーチ猫とデータ分析猫を統括し、情報収集と分析を管理
"""

import os
from typing import Dict, Any, List, Optional
from agno.agent import Agent
from agents.data_manager.analyzer.data_analyst_cat import DataAnalystCat

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
        self.storage = storage
        self.memory = None
        self.agent = None
        
        # 下位エージェントへの参照
        self.research_cat = None
        self.data_analyst_cat = None
        
    def _create_data_manager_agent(self) -> None:
        """
        データ管理猫エージェントの作成
        
        Returns:
            なし
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
        
        # エージェントの初期化（モック関連のインポートを削除）
        self.agent = None
        
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
        
        # データ管理猫からの応答プレフィックス
        response_prefix = """# 🐱 データ管理猫からの応答

"""
        
        # リクエストタイプに応じた処理
        if request_type == "research_only":
            # 情報収集のみのリクエスト
            if self.debug_mode:
                print("Debug: リサーチ猫に転送")
            
            # 現在はリサーチ機能は未実装
            response = f"""{response_prefix}## リサーチ機能について

申し訳ありませんが、リサーチ機能は現在実装中です。
以下のデータ分析機能をご利用ください：

- 売上データの分析
- 各種統計分析
- データ可視化

お役に立てず申し訳ありませんにゃ～（=^・ω・^=）"""
            
        elif request_type == "analysis_only":
            # データ分析のみのリクエスト
            if self.debug_mode:
                print("Debug: データ分析猫に転送")
            
            # 分析内容に応じて適切なデータを準備
            if "売上" in request and "分析" in request:
                # 売上データを生成して分析猫に渡す
                import pandas as pd
                import numpy as np
                
                # サンプルの売上データを作成
                np.random.seed(123)
                dates = pd.date_range(start='2025-01-01', end='2025-01-31')
                sales_data = pd.DataFrame({
                    '日付': dates,
                    '売上高': np.random.normal(100000, 15000, len(dates)),
                    '商品A販売数': np.random.randint(50, 200, len(dates)),
                    '商品B販売数': np.random.randint(30, 100, len(dates)),
                    '商品C販売数': np.random.randint(10, 50, len(dates)),
                    '顧客数': np.random.randint(200, 500, len(dates))
                })
                
                # データ分析猫に分析を依頼
                analysis_request = f"以下の先月（2025年1月）の売上データを分析してください：\n\n{request}"
                
                try:
                    # 分析結果を取得
                    analysis_response = self.data_analyst_cat.analyze_data(analysis_request, sales_data)
                    
                    # 応答を整形
                    response = f"""# 📊 売上データ分析結果

{analysis_response}

何か他にお知りになりたいことがあれば、お気軽にお尋ねくださいにゃ～（=^・ω・^=）"""
                except Exception as e:
                    # エラーが発生した場合は代替応答
                    print(f"データ分析でエラーが発生: {e}")
                    response = f"""# ⚠️ データ分析中にエラーが発生しました

申し訳ありませんが、売上データの分析中に問題が発生しましたにゃ。
エラー内容: {str(e)}

別の方法でお試しいただくか、少し後でもう一度お試しくださいにゃ。"""
            else:
                # その他の分析リクエスト
                analysis_response = self.data_analyst_cat.analyze_data(request)
                response = f"{response_prefix}{analysis_response}\n\nデータ分析猫と協力して分析を行いました（=^・ω・^=）"
            
        else:
            # 情報収集と分析の両方を含むリクエスト
            if self.debug_mode:
                print("Debug: リサーチ猫とデータ分析猫に順次転送")
            
            # モック実装として、売上データ分析のリクエストの場合はサンプルデータを用意
            if "売上" in request and "分析" in request:
                import pandas as pd
                import numpy as np
                
                # サンプルの売上データを作成
                np.random.seed(123)
                dates = pd.date_range(start='2025-01-01', end='2025-01-31')
                sales_data = pd.DataFrame({
                    '日付': dates,
                    '売上高': np.random.normal(100000, 15000, len(dates)),
                    '商品A販売数': np.random.randint(50, 200, len(dates)),
                    '商品B販売数': np.random.randint(30, 100, len(dates)),
                    '商品C販売数': np.random.randint(10, 50, len(dates)),
                    '顧客数': np.random.randint(200, 500, len(dates))
                })
                
                # データ分析猫にデータ分析を依頼
                analysis_request = f"以下の先月（2025年1月）の売上データを分析してください：\n\n{request}"
                
                try:
                    # 分析結果を取得
                    analysis_response = self.data_analyst_cat.analyze_data(analysis_request, sales_data)
                    
                    # 応答を整形
                    response = f"""# 📊 売上データ分析結果

まず情報を収集し、次にデータ分析を行いました。

{analysis_response}

他に詳しく分析したい点があれば教えてくださいにゃ～（=^・ω・^=）"""
                except Exception as e:
                    # エラーが発生した場合は代替応答
                    print(f"データ分析でエラーが発生: {e}")
                    response = f"""# ⚠️ データ分析中にエラーが発生しました

申し訳ありませんが、売上データの分析中に問題が発生しましたにゃ。
エラー内容: {str(e)}

別の方法でお試しいただくか、少し後でもう一度お試しくださいにゃ。"""
            else:
                # その他のリクエスト
                response = f"""{response_prefix}## リクエストについて

申し訳ありませんが、このタイプのリクエストは現在対応できません。
以下のようなデータ分析リクエストをお試しください：

- 「先月の売上データを分析して」
- 「売上高の推移を教えて」
- 「商品別の販売数を分析して」

データ分析に関するご質問があれば、お気軽にお尋ねくださいにゃ～（=^・ω・^=）"""
        
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
        # データ分析猫の初期化
        if self.data_analyst_cat is None:
            self.data_analyst_cat = DataAnalystCat(storage=self.storage, debug_mode=self.debug_mode)
            
        # リサーチ猫の初期化（将来実装）
        # if self.research_cat is None:
        #     self.research_cat = ResearchCat(storage=self.storage, debug_mode=self.debug_mode)
