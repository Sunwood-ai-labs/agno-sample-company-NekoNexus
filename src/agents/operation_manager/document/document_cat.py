#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ドキュメント作成猫 - 文書作成エージェント
メール文案猫とレポート作成猫を統括し、文書作成を担当
"""

import os
from typing import Dict, Any, List, Optional
from utils.agno_mock import Agent, AgentMemory, create_agent, SqliteAgentStorage

class DocumentCat:
    """
    ドキュメント作成猫クラス
    文書作成を担当するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        ドキュメント作成猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_document_agent()
        
        # ドキュメントテンプレート
        self.templates = {
            "email": {
                "business": "件名: {subject}\n\n{recipient}様\n\n{greeting}\n\n{body}\n\n{closing}\n\n{sender_name}\n{sender_title}\n{sender_contact}",
                "internal": "件名: {subject}\n\n{recipient}様\n\n{body}\n\n{sender_name}",
                "inquiry": "件名: {subject}\n\n{recipient}様\n\n{greeting}\n\n以下の件につきましてお問い合わせ申し上げます。\n\n{body}\n\n{closing}\n\n{sender_name}\n{sender_title}\n{sender_contact}"
            },
            "report": {
                "business": "# {title}\n\n## 概要\n{summary}\n\n## 背景\n{background}\n\n## 詳細\n{details}\n\n## 結論\n{conclusion}\n\n## 推奨事項\n{recommendations}",
                "weekly": "# {title}\n\n## 期間\n{period}\n\n## 達成事項\n{achievements}\n\n## 進行中の作業\n{in_progress}\n\n## 課題\n{issues}\n\n## 来週の計画\n{next_week_plan}"
            }
        }
        
        # 下位エージェントへの参照
        self.email_cat = None
        self.report_cat = None
        
    def _create_document_agent(self) -> Agent:
        """
        ドキュメント作成猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「ドキュメント作成猫」という名前の猫猫カンパニーの文書作成AIエージェントです。
        メール文案猫とレポート作成猫を統括し、様々な種類の文書を作成する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. 業務遂行猫からの文書作成リクエストを理解する
        2. リクエストに応じて適切な文書種別（メール、レポート等）を判断する
        3. メール文案猫またはレポート作成猫に適切な作成指示を出す
        4. 作成された文書を確認・編集する
        5. 業務遂行猫に作成結果を報告する
        
        文書作成の際は以下の点に注意してください：
        1. 目的と対象読者を明確に意識する
        2. 正確さ、明確さ、簡潔さを心がける
        3. 猫猫カンパニーの企業文化や価値観を反映する
        4. 必要に応じて敬語や専門用語を適切に使用する
        5. 文法や表現の誤りがないよう注意する
        
        回答は常に日本語で行い、作成した文書を中心に提示してください。
        また、猫らしい丁寧で文学的な口調を使用してください。
        例: 「～にゃ」「～でございますにゃん」などの表現を適度に使用。
        
        作成した文書は以下の形式で提示してください：
        1. 文書の種類と目的
        2. 作成した文書の本文
        3. 補足説明や使用上の注意点（該当する場合）
        
        それぞれの文書種別における特徴と注意点：
        
        【メール】
        - ビジネスメール: 正式で丁寧な表現、敬語の適切な使用
        - 社内メール: やや砕けた表現も可、要点を簡潔に
        - お問い合わせメール: 具体的な内容と回答期待時期を明記
        
        【レポート】
        - ビジネスレポート: 論理的構成、データや事実に基づく記述
        - 週次報告: 簡潔な要約、達成事項と課題の明確化
        - プレゼン資料: 視覚的に理解しやすい構成、要点の強調
        """
        
        return create_agent(
            id="document_cat",
            model="gpt-4o",
            description="ドキュメント作成猫 - メール文案猫とレポート作成猫を統括し、文書作成を担当。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def create_document(self, request: str, document_type: Optional[str] = None) -> str:
        """
        文書作成リクエストを処理する
        
        Args:
            request: 業務遂行猫からのリクエスト文字列
            document_type: 文書の種類を明示的に指定（指定がない場合は自動判別）
            
        Returns:
            作成した文書の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: ドキュメント作成猫へのリクエスト: {request}")
            if document_type:
                print(f"Debug: 指定された文書タイプ: {document_type}")
        
        # 文書タイプが明示されていない場合は判断
        if not document_type:
            document_type = self._determine_document_type(request)
            if self.debug_mode:
                print(f"Debug: 判断された文書タイプ: {document_type}")
        
        # 文書タイプに基づいて適切なテンプレートを提示
        template_info = ""
        if document_type == "email":
            template_info = """
            メールテンプレートの基本構造:
            - 件名: 簡潔で内容を表すもの
            - 宛先: 相手の名前と敬称
            - 挨拶: 季節や時候の挨拶（適宜）
            - 本文: 要件を明確に
            - 締めの言葉: 結びの挨拶
            - 署名: 送信者情報
            """
        elif document_type == "report":
            template_info = """
            レポートテンプレートの基本構造:
            - タイトル: 内容を表す明確なもの
            - 概要: 内容の要約（エグゼクティブサマリー）
            - 背景: 経緯や目的
            - 詳細: 本文（データや事実に基づく記述）
            - 結論: 得られた知見や結果
            - 推奨事項: 提案や次のステップ
            """
        elif document_type == "meeting":
            template_info = """
            会議資料テンプレートの基本構造:
            - タイトル: 会議の目的
            - 日時・場所: 会議の実施情報
            - 参加者: メンバーリスト
            - アジェンダ: 議題と時間配分
            - 資料本体: 説明内容
            - アクションアイテム: 会議後のタスク
            """
        
        # テンプレート情報を含めたリクエスト
        enhanced_request = f"{request}\n\n{template_info}"
        
        # 文書作成の実行
        response = self.agent.message(enhanced_request)
        
        return response
    
    def _determine_document_type(self, request: str) -> str:
        """
        リクエストから文書の種類を判断する
        
        Args:
            request: リクエスト文字列
            
        Returns:
            文書タイプ: "email", "report", "meeting", "other"のいずれか
        """
        # メール関連のキーワード
        email_keywords = ["メール", "email", "mail", "Eメール", "メッセージ", "返信", "送信"]
        
        # レポート関連のキーワード
        report_keywords = ["レポート", "report", "報告書", "報告", "レポ", "文書", "ドキュメント"]
        
        # 会議資料関連のキーワード
        meeting_keywords = ["会議", "meeting", "ミーティング", "資料", "議事録", "アジェンダ", "プレゼン"]
        
        # キーワードマッチング
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in email_keywords):
            return "email"
        elif any(keyword in request_lower for keyword in report_keywords):
            return "report"
        elif any(keyword in request_lower for keyword in meeting_keywords):
            return "meeting"
        else:
            return "other"
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
