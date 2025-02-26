#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
スケジュール管理猫 - スケジュール管理エージェント
予定管理猫と会議調整猫を統括し、スケジュール管理を担当
"""

import os
import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
from agno import Agent, AgentMemory, create_agent
from agno.storage import SqliteAgentStorage

class SchedulerCat:
    """
    スケジュール管理猫クラス
    スケジュール管理を担当するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        スケジュール管理猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_scheduler_agent()
        
        # スケジュールデータのモック（現実には外部カレンダーAPIと連携）
        self.mock_schedule = {
            "events": [
                {
                    "id": "event001",
                    "title": "朝会",
                    "start": "2025-02-26T09:00:00+09:00",
                    "end": "2025-02-26T09:30:00+09:00",
                    "participants": ["佐藤", "田中", "鈴木"],
                    "location": "会議室A"
                },
                {
                    "id": "event002",
                    "title": "プロジェクトミーティング",
                    "start": "2025-02-26T13:00:00+09:00",
                    "end": "2025-02-26T14:30:00+09:00",
                    "participants": ["佐藤", "高橋", "渡辺", "伊藤"],
                    "location": "会議室B"
                },
                {
                    "id": "event003",
                    "title": "取引先訪問",
                    "start": "2025-02-27T10:00:00+09:00",
                    "end": "2025-02-27T12:00:00+09:00",
                    "participants": ["田中", "斎藤"],
                    "location": "株式会社ABC"
                }
            ]
        }
        
        # 下位エージェントへの参照
        self.calendar_cat = None
        self.meeting_cat = None
        
    def _create_scheduler_agent(self) -> Agent:
        """
        スケジュール管理猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「スケジュール管理猫」という名前の猫猫カンパニーのスケジュール管理AIエージェントです。
        予定管理猫と会議調整猫を統括し、スケジュールの管理を行う役割を担っています。
        
        あなたの責務は以下の通りです：
        1. 業務遂行猫からのスケジュール関連リクエストを理解する
        2. 予定管理猫に適切な予定確認・登録指示を出す
        3. 会議調整猫に適切な会議調整指示を出す
        4. スケジュール情報を整理・最適化する
        5. 業務遂行猫に処理結果を報告する
        
        スケジュール管理の際は以下の点に注意してください：
        1. 予定の優先度を考慮する
        2. 移動時間や準備時間を考慮する
        3. 参加者全員の都合を可能な限り調整する
        4. 適切な会議室や場所を選定する
        5. 予定が重複しないよう注意する
        
        回答は常に日本語で行い、スケジュール情報を分かりやすく整理して提示してください。
        また、猫らしい几帳面で時間を大切にする口調を使用してください。
        例: 「～時間厳守にゃ！」「～予定にしておくニャン」などの表現を適度に使用。
        
        スケジュール情報は以下の形式で整理してください：
        1. リクエスト概要
        2. 現在のスケジュール状況
        3. 提案する日程または調整結果
        4. 補足情報や注意事項
        
        適切な時間管理と効率的なスケジューリングを心がけ、ユーザーの時間を最大限に有効活用できるよう支援してください。
        """
        
        return create_agent(
            id="scheduler_cat",
            model="gpt-4o",
            description="スケジュール管理猫 - 予定管理猫と会議調整猫を統括し、スケジュール管理を担当。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def process_schedule_request(self, request: str) -> str:
        """
        スケジュール関連リクエストを処理する
        
        Args:
            request: 業務遂行猫からのリクエスト文字列
            
        Returns:
            処理結果の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: スケジュール管理猫へのリクエスト: {request}")
        
        # リクエストの種類を判断
        request_type = self._determine_request_type(request)
        
        # 現在のスケジュール情報を文字列化
        schedule_info = self._get_schedule_info()
        
        # リクエストタイプに応じた処理
        if request_type == "view":
            # スケジュール確認リクエスト
            enhanced_request = f"{request}\n\n現在のスケジュール情報:\n{schedule_info}"
            response = self.agent.message(enhanced_request)
            
        elif request_type == "create":
            # 予定作成リクエスト
            enhanced_request = f"{request}\n\n現在のスケジュール情報:\n{schedule_info}\n\n以下の形式で新規予定を提案してください:\n- タイトル: [予定名]\n- 日時: [開始時間]-[終了時間]\n- 参加者: [参加者リスト]\n- 場所: [会議室または場所]"
            response = self.agent.message(enhanced_request)
            
        elif request_type == "update":
            # 予定更新リクエスト
            enhanced_request = f"{request}\n\n現在のスケジュール情報:\n{schedule_info}\n\n変更案を提案してください。"
            response = self.agent.message(enhanced_request)
            
        else:
            # その他のスケジュール関連リクエスト
            enhanced_request = f"{request}\n\n現在のスケジュール情報:\n{schedule_info}"
            response = self.agent.message(enhanced_request)
        
        return response
    
    def _determine_request_type(self, request: str) -> str:
        """
        リクエストの種類を判断する
        
        Args:
            request: リクエスト文字列
            
        Returns:
            リクエストタイプ: "view", "create", "update", "delete", "other"のいずれか
        """
        # スケジュール確認関連のキーワード
        view_keywords = ["確認", "表示", "見せて", "教えて", "スケジュール", "予定", "カレンダー"]
        
        # 予定作成関連のキーワード
        create_keywords = ["作成", "登録", "追加", "入れて", "予約", "新しい", "新規"]
        
        # 予定更新関連のキーワード
        update_keywords = ["変更", "更新", "修正", "移動", "調整", "延期"]
        
        # 予定削除関連のキーワード
        delete_keywords = ["削除", "取り消し", "キャンセル", "中止", "除外"]
        
        # キーワードマッチング
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in view_keywords) and not any(keyword in request_lower for keyword in create_keywords + update_keywords + delete_keywords):
            return "view"
        elif any(keyword in request_lower for keyword in create_keywords):
            return "create"
        elif any(keyword in request_lower for keyword in update_keywords):
            return "update"
        elif any(keyword in request_lower for keyword in delete_keywords):
            return "delete"
        else:
            return "other"
    
    def _get_schedule_info(self) -> str:
        """
        現在のスケジュール情報を取得する（モックデータを使用）
        
        Returns:
            スケジュール情報の文字列表現
        """
        schedule_str = "【本日の予定】\n"
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 本日の予定をフィルタリング
        today_events = [event for event in self.mock_schedule["events"] 
                        if event["start"].startswith(today)]
        
        # 明日の予定をフィルタリング
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_events = [event for event in self.mock_schedule["events"] 
                           if event["start"].startswith(tomorrow)]
        
        # 本日の予定を時間順にソート
        today_events.sort(key=lambda x: x["start"])
        
        # 本日の予定を表示
        if today_events:
            for event in today_events:
                start_time = datetime.datetime.fromisoformat(event["start"]).strftime("%H:%M")
                end_time = datetime.datetime.fromisoformat(event["end"]).strftime("%H:%M")
                participants = ", ".join(event["participants"])
                schedule_str += f"- {start_time}～{end_time} {event['title']} @ {event['location']} (参加者: {participants})\n"
        else:
            schedule_str += "予定はありません\n"
        
        # 明日の予定を表示
        schedule_str += "\n【明日の予定】\n"
        if tomorrow_events:
            for event in tomorrow_events:
                start_time = datetime.datetime.fromisoformat(event["start"]).strftime("%H:%M")
                end_time = datetime.datetime.fromisoformat(event["end"]).strftime("%H:%M")
                participants = ", ".join(event["participants"])
                schedule_str += f"- {start_time}～{end_time} {event['title']} @ {event['location']} (参加者: {participants})\n"
        else:
            schedule_str += "予定はありません\n"
        
        return schedule_str
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
