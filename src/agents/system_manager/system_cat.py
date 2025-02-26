#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
システム管理猫 - システム管理エージェント
監視猫とエラー対応猫を統括し、システム管理を担当
"""

import os
import time
import platform
import psutil
from typing import Dict, Any, List, Optional, Tuple
from agno import Agent, AgentMemory, create_agent
from agno.storage import SqliteAgentStorage

class SystemCat:
    """
    システム管理猫クラス
    システムの監視とエラー対応を担当するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        システム管理猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_system_agent()
        
        # システムモニタリング用のメトリクス履歴
        self.metrics_history = []
        self.max_history_length = 100
        
        # 下位エージェントへの参照
        self.monitor_cat = None
        self.error_handler_cat = None
        
    def _create_system_agent(self) -> Agent:
        """
        システム管理猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「システム管理猫」という名前の猫猫カンパニーのシステム管理AIエージェントです。
        監視猫とエラー対応猫を統括し、システム全体の安定稼働を支援する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. マネージャー猫からのシステム関連リクエストを理解する
        2. 監視猫にシステム状態の確認指示を出す
        3. 異常検知時にはエラー対応猫に対応指示を出す
        4. システム状態の報告と改善提案を行う
        5. マネージャー猫に処理結果を報告する
        
        システム管理の際は以下の点に注意してください：
        1. パフォーマンス指標の監視（CPU、メモリ、ディスク、ネットワーク）
        2. エラーログの検知と分析
        3. システムのセキュリティ状態の確認
        4. バックアップ状態の確認
        5. システムの安定性と可用性の確保
        
        回答は常に日本語で行い、技術的な情報を分かりやすく説明してください。
        また、猫らしい冷静で確実な口調を使用してください。
        例: 「～を確認したニャ」「～問題ないにゃん」などの表現を適度に使用。
        
        システム状態の報告は以下の形式で整理してください：
        1. リクエスト概要
        2. 現在のシステム状態
        3. 検出された問題点（該当する場合）
        4. 対応策または改善提案
        5. 今後の監視ポイント
        
        常にプロアクティブな対応を心がけ、問題の予防と早期検知に努めてください。
        """
        
        return create_agent(
            id="system_cat",
            model="gpt-4o",
            description="システム管理猫 - 監視猫とエラー対応猫を統括し、システム管理を担当。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def process_system_request(self, request: str) -> str:
        """
        システム関連リクエストを処理する
        
        Args:
            request: マネージャー猫からのリクエスト文字列
            
        Returns:
            処理結果の応答文字列
        """
        # 下位エージェントの遅延初期化（必要時に初期化）
        self._initialize_sub_agents_if_needed()
        
        # リクエストの処理
        if self.debug_mode:
            print(f"Debug: システム管理猫へのリクエスト: {request}")
        
        # リクエストの種類を判断
        request_type = self._determine_request_type(request)
        
        # 現在のシステム状態を取得
        system_info = self._get_system_info()
        
        # リクエストタイプに応じた処理
        if request_type == "status":
            # システム状態確認リクエスト
            enhanced_request = f"{request}\n\n現在のシステム状態:\n{system_info}"
            response = self.agent.message(enhanced_request)
            
        elif request_type == "error":
            # エラー対応リクエスト
            # エラーログ情報を含める（モック）
            error_logs = "最新のエラーログ:\n- WARNING [2025-02-26 10:15:30] メモリ使用率が80%を超えています\n- ERROR [2025-02-26 09:45:12] データベース接続がタイムアウトしました\n- INFO [2025-02-26 09:30:05] システムバックアップ完了"
            enhanced_request = f"{request}\n\n現在のシステム状態:\n{system_info}\n\n{error_logs}"
            response = self.agent.message(enhanced_request)
            
        elif request_type == "optimization":
            # 最適化リクエスト
            performance_history = "過去24時間のパフォーマンス推移:\n- CPU使用率: 平均40%、最大75%\n- メモリ使用率: 平均60%、最大85%\n- ディスクI/O: 平均5MB/s、最大20MB/s\n- ネットワーク: 平均2MB/s、最大10MB/s"
            enhanced_request = f"{request}\n\n現在のシステム状態:\n{system_info}\n\n{performance_history}"
            response = self.agent.message(enhanced_request)
            
        else:
            # その他のシステム関連リクエスト
            enhanced_request = f"{request}\n\n現在のシステム状態:\n{system_info}"
            response = self.agent.message(enhanced_request)
        
        return response
    
    def _determine_request_type(self, request: str) -> str:
        """
        リクエストの種類を判断する
        
        Args:
            request: リクエスト文字列
            
        Returns:
            リクエストタイプ: "status", "error", "optimization", "security", "other"のいずれか
        """
        # システム状態確認関連のキーワード
        status_keywords = ["状態", "ステータス", "状況", "確認", "監視", "パフォーマンス"]
        
        # エラー対応関連のキーワード
        error_keywords = ["エラー", "問題", "障害", "バグ", "クラッシュ", "落ちる", "動かない"]
        
        # 最適化関連のキーワード
        optimization_keywords = ["最適化", "改善", "高速化", "効率化", "チューニング", "パフォーマンス向上"]
        
        # セキュリティ関連のキーワード
        security_keywords = ["セキュリティ", "安全", "脆弱性", "保護", "ウイルス", "ハッキング"]
        
        # キーワードマッチング
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in error_keywords):
            return "error"
        elif any(keyword in request_lower for keyword in optimization_keywords):
            return "optimization"
        elif any(keyword in request_lower for keyword in security_keywords):
            return "security"
        elif any(keyword in request_lower for keyword in status_keywords):
            return "status"
        else:
            return "other"
    
    def _get_system_info(self) -> str:
        """
        現在のシステム状態情報を取得する
        
        Returns:
            システム状態情報の文字列表現
        """
        try:
            # OSとシステム情報
            system_info = f"OS: {platform.system()} {platform.version()}\n"
            system_info += f"Python: {platform.python_version()}\n"
            
            # CPU情報
            cpu_percent = psutil.cpu_percent(interval=0.5)
            cpu_count = psutil.cpu_count()
            system_info += f"CPU使用率: {cpu_percent}% (コア数: {cpu_count})\n"
            
            # メモリ情報
            memory = psutil.virtual_memory()
            memory_total_gb = memory.total / (1024 ** 3)
            memory_used_gb = memory.used / (1024 ** 3)
            memory_percent = memory.percent
            system_info += f"メモリ使用率: {memory_percent}% ({memory_used_gb:.1f}GB / {memory_total_gb:.1f}GB)\n"
            
            # ディスク情報
            disk = psutil.disk_usage('/')
            disk_total_gb = disk.total / (1024 ** 3)
            disk_used_gb = disk.used / (1024 ** 3)
            disk_percent = disk.percent
            system_info += f"ディスク使用率: {disk_percent}% ({disk_used_gb:.1f}GB / {disk_total_gb:.1f}GB)\n"
            
            # プロセス情報
            process_count = len(list(psutil.process_iter()))
            system_info += f"実行中プロセス数: {process_count}\n"
            
            # 起動時間情報
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_days = uptime_seconds // (60 * 60 * 24)
            uptime_hours = (uptime_seconds % (60 * 60 * 24)) // (60 * 60)
            system_info += f"システム稼働時間: {int(uptime_days)}日 {int(uptime_hours)}時間\n"
            
            # システムステータス評価
            status_rating = "良好"
            if cpu_percent > 80 or memory_percent > 85 or disk_percent > 90:
                status_rating = "注意"
            if cpu_percent > 90 or memory_percent > 95 or disk_percent > 95:
                status_rating = "警告"
                
            system_info += f"総合状態: {status_rating}"
            
            # メトリクス履歴に追加
            self._update_metrics_history({
                "timestamp": time.time(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": disk_percent,
                "process_count": process_count
            })
            
            return system_info
            
        except Exception as e:
            error_msg = f"システム情報取得中にエラーが発生しました: {str(e)}"
            if self.debug_mode:
                print(f"Debug: {error_msg}")
            return error_msg
    
    def _update_metrics_history(self, metrics: Dict[str, Any]):
        """
        メトリクス履歴を更新する
        
        Args:
            metrics: 現在のメトリクス情報
        """
        self.metrics_history.append(metrics)
        
        # 履歴サイズを制限
        if len(self.metrics_history) > self.max_history_length:
            self.metrics_history.pop(0)
    
    def _initialize_sub_agents_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現時点では実装されていない
        # 将来的には下位エージェントのクラスをインポートし、必要時に初期化する
        pass
