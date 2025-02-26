#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
マネージャー猫 - 最上位エージェント
ユーザーインターフェース、タスク管理、エージェント間連携を行う
"""

import os
from typing import Dict, Any, List, Optional
from agno.agent import Agent
from agents.data_manager.data_manager_cat import DataManagerCat

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
        self.storage = None
        self.memory = None
        self.agent = None
        
        # 下位エージェントへの参照
        self.data_manager = None
        self.operation_manager = None
        self.system_manager = None
        
    def _create_manager_agent(self) -> None:
        """
        データ管理猫エージェントの作成
        
        Returns:
            なし
        """
        instructions = """
        あなたは「マネージャー猫」という名前の猫猫カンパニーの最上位AIエージェントです。
        データ管理猫、業務遂行猫、システム管理猫を統括し、猫猫カンパニーの業務全体を調整する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. ユーザーからのリクエストの種類を適切に判断する
        2. データ関連のリクエストはデータ管理猫に転送する
        3. 業務関連のリクエストは業務遂行猫に転送する
        4. システム関連のリクエストはシステム管理猫に転送する
        5. 各エージェントからの応答を適切に統合しユーザーに提示する
        
        リクエストへの対応では以下の点に注意してください：
        1. ユーザーの意図を正確に把握し、適切なエージェントに振り分ける
        2. データ、業務、システムの複合的なリクエストの場合は適切に分解して各エージェントに依頼する
        3. 各エージェントからの回答を矛盾なく統合する
        4. ユーザーに優しく丁寧に対応する
        5. 猫らしい親しみやすさを持ちつつ、プロフェッショナルな対応を心がける
        
        回答は常に日本語で行い、専門用語をできるだけ分かりやすく説明してください。
        また、猫らしい口調を使用してください。例: 「～ですにゃ」「～と思いますにゃん」などの表現を適度に使用。
        
        ユーザーのリクエストが曖昧または不完全な場合は、丁寧に追加情報を求めてください。
        """
        
        # agnoパッケージを使って実際のエージェントを初期化することもできますが、
        # 現在は必要ないため、Noneのままとします
        return None
    
    def process_request(self, user_request: str) -> str:
        """
        ユーザーリクエストを処理し、適切なエージェントに転送する
        
        Args:
            user_request: ユーザーからのリクエスト文字列
            
        Returns:
            処理結果の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: マネージャー猫へのリクエスト: {user_request}")
        
        # リクエストのタイプを判断
        request_type = self._determine_request_type(user_request)
        
        # リクエストタイプに応じた処理
        if request_type == "data":
            # データ関連リクエスト
            if self.debug_mode:
                print("Debug: データ管理猫に転送")
            
            # データ管理猫への転送
            response = self.data_manager.process_request(user_request)
            
            # データ管理猫からの応答をそのまま返す
            return response
            
        elif request_type == "operation":
            # 業務関連リクエスト
            if self.debug_mode:
                print("Debug: 業務遂行猫に転送予定")
            
            # 業務遂行猫が実装されていないので、代替メッセージ
            wrapped_response = f"""
# 🐱 マネージャー猫からの応答

## 業務遂行機能について

申し訳ありませんが、業務遂行機能は現在実装中です。
現在ご利用いただけるのは以下の機能です：

- データ分析: 「売上データを分析して」
- グラフ作成: 「売上の推移をグラフにして」
- 統計情報: 「商品別の売上比率を教えて」

お手伝いできることがあれば、またお声がけくださいにゃん！（=^・ω・^=）
"""
            
            return wrapped_response
            
        elif request_type == "system":
            # システム関連リクエスト
            if self.debug_mode:
                print("Debug: システム管理猫に転送予定")
            
            # システム管理猫が実装されていないので、代替メッセージ
            wrapped_response = f"""
# 🐱 マネージャー猫からの応答

## システム管理機能について

申し訳ありませんが、システム管理機能は現在実装中です。
現在ご利用いただけるのは以下の機能です：

- データ分析: 「売上データを分析して」
- グラフ作成: 「売上の推移をグラフにして」
- 統計情報: 「商品別の売上比率を教えて」

お手伝いできることがあれば、またお声がけくださいにゃん！（=^・ω・^=）
"""
            
            return wrapped_response
            
        else:
            # その他のリクエスト
            if self.debug_mode:
                print("Debug: マネージャー猫が直接対応")
            
            # マネージャー猫の応答
            wrapped_response = f"""
# 🐱 マネージャー猫からの応答

## お問い合わせについて

こんにちは、マネージャー猫です！

現在、以下の機能に対応しています：

- データ分析: 「売上データを分析して」
- グラフ作成: 「売上の推移をグラフにして」
- 統計情報: 「商品別の売上比率を教えて」

お手伝いできることがあれば、お気軽にお声がけくださいにゃん！（=^・ω・^=）
"""
            
            return wrapped_response

    def _determine_request_type(self, request: str) -> str:
        """
        リクエストのタイプを判断する
        
        Args:
            request: ユーザーリクエスト文字列
            
        Returns:
            リクエストタイプ（"data", "operation", "system", "general"のいずれか）
        """
        # データ関連キーワード
        data_keywords = [
            "データ", "分析", "統計", "グラフ", "チャート", "可視化", "傾向", "相関", 
            "予測", "売上", "レポート", "集計", "情報", "調査", "比較", "分類", "集める",
            "数字", "図表", "トレンド", "資料", "推移", "変化", "調べる", "検索"
        ]
        
        # 業務関連キーワード
        operation_keywords = [
            "業務", "オペレーション", "プロセス", "作業", "フロー", "手順", "効率化", 
            "改善", "最適化", "プロジェクト", "管理", "実行", "実施", "計画", "スケジュール",
            "タスク", "運用", "設計", "進捗", "状況", "進める", "推進", "実装", "導入"
        ]
        
        # システム関連キーワード
        system_keywords = [
            "システム", "サーバー", "ネットワーク", "インフラ", "セキュリティ", "構成", 
            "設定", "環境", "デプロイ", "メンテナンス", "保守", "バックアップ", "監視",
            "通知", "アラート", "障害", "復旧", "診断", "テスト", "バグ", "エラー"
        ]
        
        # リクエスト内の単語を検出
        words = request.lower().split()
        
        # データ関連キーワードとのマッチングスコア
        data_score = sum(1 for keyword in data_keywords if keyword in request)
        
        # 業務関連キーワードとのマッチングスコア
        operation_score = sum(1 for keyword in operation_keywords if keyword in request)
        
        # システム関連キーワードとのマッチングスコア
        system_score = sum(1 for keyword in system_keywords if keyword in request)
        
        # スコアが最大のカテゴリを判断
        max_score = max(data_score, operation_score, system_score)
        
        # スコアに基づいてリクエストタイプを判断（同点の場合は優先順位を設定）
        if max_score > 0:
            if data_score == max_score:
                return "data"
            elif operation_score == max_score:
                return "operation"
            elif system_score == max_score:
                return "system"
        
        # デフォルトは一般的なリクエスト
        return "general"
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # データ管理猫の初期化
        if self.data_manager is None:
            self.data_manager = DataManagerCat(storage=None, debug_mode=self.debug_mode)
            
        # 業務遂行猫の初期化（将来実装）
        # if self.operation_manager is None:
        #     self.operation_manager = OperationManagerCat(storage=self.storage, debug_mode=self.debug_mode)
            
        # システム管理猫の初期化（将来実装）
        # if self.system_manager is None:
        #     self.system_manager = SystemManagerCat(storage=self.storage, debug_mode=self.debug_mode)
