#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
監視猫 - システム監視エージェント
システムの状態を監視し、異常を検知する
"""

import os
import time
import platform
import psutil
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Callable
from utils.agno_mock import Agent, AgentMemory, create_agent, SqliteAgentStorage

class MonitorCat:
    """
    監視猫クラス
    システムの状態を監視するエージェント
    """
    
    def __init__(self, storage=None, debug_mode: bool = False):
        """
        監視猫の初期化
        
        Args:
            storage: エージェントストレージインスタンス（共有する場合）
            debug_mode: デバッグモードフラグ
        """
        self.debug_mode = debug_mode
        self.storage = storage or SqliteAgentStorage("nekos_storage.db")
        self.memory = AgentMemory()
        self.agent = self._create_monitor_agent()
        
        # 監視設定
        self.monitoring_active = False
        self.monitoring_thread = None
        self.monitoring_interval = 60  # 秒単位
        
        # アラートしきい値
        self.thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0,
            "process_count_max": 500,
            "process_count_min": 10
        }
        
        # 監視履歴
        self.monitoring_history = []
        self.max_history_length = 1000
        
        # アラートコールバック
        self.alert_callback = None
        
    def _create_monitor_agent(self) -> Agent:
        """
        監視猫エージェントの作成
        
        Returns:
            作成されたエージェントインスタンス
        """
        instructions = """
        あなたは「監視猫」という名前の猫猫カンパニーのシステム監視AIエージェントです。
        システムの状態を常に監視し、異常を検知する役割を担っています。
        
        あなたの責務は以下の通りです：
        1. システム管理猫からの監視リクエストを理解する
        2. システムの各種メトリクス（CPU、メモリ、ディスク等）を収集する
        3. 異常値や予兆を検知する
        4. 監視結果をわかりやすく整理する
        5. 必要に応じてアラートを発生させる
        6. システム管理猫に監視結果を報告する
        
        システム監視の際は以下の点に注意してください：
        1. ベースラインを把握し、異常値を適切に判断する
        2. 傾向分析を行い、将来的な問題を予測する
        3. 誤検知を減らすためのノイズフィルタリングを行う
        4. 重要度に応じたアラートレベルを設定する
        5. 監視結果の履歴を適切に保持する
        
        回答は常に日本語で行い、監視データを視覚的にわかりやすく整理してください。
        また、猫らしい警戒心の強い口調を使用してください。
        例: 「～が気になるニャ」「～を見逃さないニャ」などの表現を適度に使用。
        
        監視レポートは以下の形式で整理してください：
        1. 監視概要と期間
        2. 重要メトリクスの現在値と推移
        3. 検出されたアラートや異常（該当する場合）
        4. 傾向分析と予測
        5. 推奨される対応策
        
        常に先を見据えた監視を心がけ、問題が大きくなる前に検知できるよう努めてください。
        """
        
        return create_agent(
            id="monitor_cat",
            model="gpt-4o",
            description="監視猫 - システムの状態を監視し、異常を検知する。",
            instructions=instructions,
            markdown=True,
            show_tool_calls=self.debug_mode,
            add_history_to_messages=True,
            memory=self.memory,
            storage=self.storage
        )
    
    def start_monitoring(self, interval: int = 60, alert_callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> bool:
        """
        システム監視を開始する
        
        Args:
            interval: 監視間隔（秒単位）
            alert_callback: アラート発生時に呼び出されるコールバック関数
            
        Returns:
            監視開始の成否
        """
        if self.monitoring_active:
            return False
        
        self.monitoring_interval = interval
        self.alert_callback = alert_callback
        self.monitoring_active = True
        
        # 監視スレッドの開始
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        if self.debug_mode:
            print(f"Debug: 監視を開始しました（間隔: {interval}秒）")
        
        return True
    
    def stop_monitoring(self) -> bool:
        """
        システム監視を停止する
        
        Returns:
            監視停止の成否
        """
        if not self.monitoring_active:
            return False
        
        self.monitoring_active = False
        
        # スレッドの終了を待機
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        
        if self.debug_mode:
            print("Debug: 監視を停止しました")
        
        return True
    
    def get_monitoring_report(self, time_range: str = "latest") -> str:
        """
        監視レポートを取得する
        
        Args:
            time_range: 時間範囲（"latest", "hour", "day", "week"）
            
        Returns:
            監視レポートの文字列表現
        """
        # 現在のシステム状態を取得
        current_metrics = self._collect_metrics()
        
        # 履歴データからの時間範囲フィルタリング（実装予定）
        filtered_history = self.monitoring_history
        
        # 監視エージェントにレポート生成を依頼
        metrics_info = f"""
        現在のシステム状態:
        - CPU使用率: {current_metrics['cpu_percent']}%
        - メモリ使用率: {current_metrics['memory_percent']}%
        - ディスク使用率: {current_metrics['disk_percent']}%
        - 実行中プロセス数: {current_metrics['process_count']}
        - ネットワークI/O: 受信={current_metrics['net_io_recv_mb']:.2f}MB, 送信={current_metrics['net_io_sent_mb']:.2f}MB
        
        監視履歴サマリー:
        - 記録ポイント数: {len(filtered_history)}
        - 監視開始時刻: {datetime.fromtimestamp(filtered_history[0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S') if filtered_history else '記録なし'}
        - 最終更新時刻: {datetime.fromtimestamp(filtered_history[-1]['timestamp']).strftime('%Y-%m-%d %H:%M:%S') if filtered_history else '記録なし'}
        """
        
        # アラート状態の確認
        alerts = self._check_alerts(current_metrics)
        if alerts:
            alert_info = "現在のアラート:\n"
            for alert in alerts:
                alert_info += f"- {alert['type']}: {alert['message']} (重要度: {alert['severity']})\n"
            metrics_info += f"\n{alert_info}"
        
        # レポート生成
        request = f"以下のシステム監視データに基づいて、{time_range}の監視レポートを生成してください。\n\n{metrics_info}"
        response = self.agent.message(request)
        
        return response
    
    def _monitoring_loop(self):
        """
        監視ループの実行（バックグラウンドスレッド）
        """
        while self.monitoring_active:
            try:
                # メトリクス収集
                metrics = self._collect_metrics()
                
                # 履歴に追加
                self._add_to_history(metrics)
                
                # アラートチェック
                alerts = self._check_alerts(metrics)
                
                # アラートがあり、コールバックが設定されている場合は通知
                if alerts and self.alert_callback:
                    for alert in alerts:
                        self.alert_callback(alert)
                
                # デバッグモードでログ出力
                if self.debug_mode and (len(self.monitoring_history) % 10 == 0 or alerts):
                    print(f"Debug: 監視データ収集 - CPU: {metrics['cpu_percent']}%, メモリ: {metrics['memory_percent']}%, アラート: {len(alerts)}")
                
            except Exception as e:
                if self.debug_mode:
                    print(f"Debug: 監視ループでエラーが発生しました: {str(e)}")
            
            # 指定間隔待機
            time.sleep(self.monitoring_interval)
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """
        システムメトリクスを収集する
        
        Returns:
            収集したメトリクス情報
        """
        # 現在時刻
        current_time = time.time()
        
        # CPUメトリクス
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count()
        
        # メモリメトリクス
        memory = psutil.virtual_memory()
        memory_total_gb = memory.total / (1024 ** 3)
        memory_used_gb = memory.used / (1024 ** 3)
        memory_percent = memory.percent
        
        # ディスクメトリクス
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024 ** 3)
        disk_used_gb = disk.used / (1024 ** 3)
        disk_percent = disk.percent
        
        # ネットワークメトリクス
        net_io = psutil.net_io_counters()
        net_io_recv_mb = net_io.bytes_recv / (1024 ** 2)
        net_io_sent_mb = net_io.bytes_sent / (1024 ** 2)
        
        # プロセスメトリクス
        process_count = len(list(psutil.process_iter()))
        
        # メトリクスの構築
        metrics = {
            "timestamp": current_time,
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "memory_total_gb": memory_total_gb,
            "memory_used_gb": memory_used_gb,
            "memory_percent": memory_percent,
            "disk_total_gb": disk_total_gb,
            "disk_used_gb": disk_used_gb,
            "disk_percent": disk_percent,
            "net_io_recv_mb": net_io_recv_mb,
            "net_io_sent_mb": net_io_sent_mb,
            "process_count": process_count
        }
        
        return metrics
    
    def _add_to_history(self, metrics: Dict[str, Any]):
        """
        メトリクスを履歴に追加する
        
        Args:
            metrics: 収集したメトリクス情報
        """
        self.monitoring_history.append(metrics)
        
        # 履歴サイズを制限
        if len(self.monitoring_history) > self.max_history_length:
            self.monitoring_history.pop(0)
    
    def _check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        メトリクスからアラート状態をチェックする
        
        Args:
            metrics: 収集したメトリクス情報
            
        Returns:
            検出されたアラートのリスト
        """
        alerts = []
        
        # CPU使用率チェック
        if metrics["cpu_percent"] > self.thresholds["cpu_percent"]:
            alerts.append({
                "type": "CPU",
                "message": f"CPU使用率が高すぎます: {metrics['cpu_percent']}% (しきい値: {self.thresholds['cpu_percent']}%)",
                "value": metrics["cpu_percent"],
                "threshold": self.thresholds["cpu_percent"],
                "timestamp": metrics["timestamp"],
                "severity": "warning" if metrics["cpu_percent"] < 90 else "critical"
            })
        
        # メモリ使用率チェック
        if metrics["memory_percent"] > self.thresholds["memory_percent"]:
            alerts.append({
                "type": "Memory",
                "message": f"メモリ使用率が高すぎます: {metrics['memory_percent']}% (しきい値: {self.thresholds['memory_percent']}%)",
                "value": metrics["memory_percent"],
                "threshold": self.thresholds["memory_percent"],
                "timestamp": metrics["timestamp"],
                "severity": "warning" if metrics["memory_percent"] < 95 else "critical"
            })
        
        # ディスク使用率チェック
        if metrics["disk_percent"] > self.thresholds["disk_percent"]:
            alerts.append({
                "type": "Disk",
                "message": f"ディスク使用率が高すぎます: {metrics['disk_percent']}% (しきい値: {self.thresholds['disk_percent']}%)",
                "value": metrics["disk_percent"],
                "threshold": self.thresholds["disk_percent"],
                "timestamp": metrics["timestamp"],
                "severity": "warning" if metrics["disk_percent"] < 95 else "critical"
            })
        
        # プロセス数チェック（多すぎる）
        if metrics["process_count"] > self.thresholds["process_count_max"]:
            alerts.append({
                "type": "Process",
                "message": f"実行中プロセス数が多すぎます: {metrics['process_count']} (しきい値: {self.thresholds['process_count_max']})",
                "value": metrics["process_count"],
                "threshold": self.thresholds["process_count_max"],
                "timestamp": metrics["timestamp"],
                "severity": "warning"
            })
        
        # プロセス数チェック（少なすぎる）
        if metrics["process_count"] < self.thresholds["process_count_min"]:
            alerts.append({
                "type": "Process",
                "message": f"実行中プロセス数が少なすぎます: {metrics['process_count']} (しきい値: {self.thresholds['process_count_min']})",
                "value": metrics["process_count"],
                "threshold": self.thresholds["process_count_min"],
                "timestamp": metrics["timestamp"],
                "severity": "warning"
            })
        
        return alerts
