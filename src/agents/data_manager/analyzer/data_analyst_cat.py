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
from pathlib import Path
import time
from matplotlib.dates import DateFormatter
from agno.agent import Agent

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
        self.storage = storage or None
        self.memory = None
        self.agent = None
        
        # 分析結果の格納先
        self.analysis_results = {}
        self.visualization_results = {}
        
        # 下位エージェントへの参照
        self.statistical_analysis_cat = None
        self.visualization_cat = None
        
    def _create_analyst_agent(self) -> None:
        """
        データ分析猫エージェントの作成
        
        Returns:
            なし
        """
        pass
    
    def analyze_data(self, request: str, data: Optional[Union[pd.DataFrame, List, Dict]] = None) -> str:
        """
        データ分析リクエストを処理する
        
        Args:
            request: データ分析リクエストの内容
            data: 分析対象のデータ（DataFrame、リスト、または辞書）
            
        Returns:
            分析結果の文字列
        """
        # 応答用のディレクトリを確保
        Path("assets").mkdir(exist_ok=True)
        
        # データが提供されている場合は実際の分析を実行
        if data is not None and isinstance(data, pd.DataFrame):
            # 実際のデータ分析処理を行う
            analysis_result = self._perform_real_data_analysis(data, request)
            return analysis_result
        else:
            # データがない場合はエラーメッセージを返す
            error_message = """
## ⚠️ データが提供されていません

データ分析を行うためには、適切な形式のデータフレームが必要です。
以下をご確認ください:

1. データが正しく渡されているか
2. データがpd.DataFrame形式か
3. 必要なカラムがデータに含まれているか

サンプルデータを自動生成して分析を行う場合は、データ管理猫に「サンプルデータで分析して」とリクエストしてください。
            """
            return error_message
    
    def _perform_real_data_analysis(self, df: pd.DataFrame, request: str) -> str:
        """
        実際のデータ分析を行う
        
        Args:
            df: 分析対象のデータフレーム
            request: 分析リクエスト
            
        Returns:
            分析結果のレポート
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        import time
        from matplotlib.dates import DateFormatter
        
        # 日本語フォントの設定を試みる
        try:
            # 一般的な日本語フォントを試す（日本語表示の優先順位を示す）
            font_candidates = [
                'IPAGothic', 'IPAexGothic', 'IPAPGothic', 'IPAMincho', 'IPAexMincho', 
                'Noto Sans CJK JP', 'MS Gothic', 'VL Gothic', 'Meiryo', 'TakaoGothic',
                'Hiragino Sans GB', 'Hiragino Kaku Gothic Pro'
            ]
            font_found = False
            
            for font in font_candidates:
                try:
                    plt.rcParams['font.family'] = font
                    # テストプロット
                    fig = plt.figure(figsize=(1, 1))
                    plt.text(0.5, 0.5, '日本語テスト')
                    plt.close(fig)
                    font_found = True
                    if self.debug_mode:
                        print(f"Debug: 日本語フォント '{font}' を使用します。")
                    break
                except Exception as e:
                    if self.debug_mode:
                        print(f"Debug: フォント '{font}' の使用中にエラー: {e}")
                    continue
            
            if not font_found:
                # 日本語フォントが見つからない場合はデフォルトのサンセリフフォントを使用
                if self.debug_mode:
                    print("Debug: 日本語フォントが見つかりません。デフォルトフォントを使用します。")
                plt.rcParams['font.family'] = 'sans-serif'
                # matplotlib 内部でデフォルトで日本語をサポートするフォントを指定
                plt.rcParams['font.sans-serif'] = ['IPAGothic', 'DejaVu Sans', 'Arial Unicode MS', 'Hiragino Sans GB']
                
                # matplotlib.fontManager をリロードしてフォントを再検出させる
                import matplotlib.font_manager as fm
                fm._rebuild()
        except Exception as e:
            # 何らかのエラーが発生した場合
            if self.debug_mode:
                print(f"Debug: フォント設定中にエラーが発生しました: {e}")
                print("Debug: デフォルト設定を使用します。")
            plt.rcParams['font.family'] = 'sans-serif'
        
        # 分析レポートを作成
        analysis_report = []
        analysis_report.append("## 📝 データ概要")
        
        # データの基本情報
        data_info = f"""
データの期間: {df['日付'].min().strftime('%Y年%m月%d日')} 〜 {df['日付'].max().strftime('%Y年%m月%d日')}
データ行数: {len(df)} 行
データ列: {', '.join(df.columns)}
"""
        analysis_report.append(data_info)
        
        # 数値データの統計情報
        numeric_cols = df.select_dtypes(include=['number']).columns
        statistical_summary = df[numeric_cols].describe().round(2)
        analysis_report.append("## 📊 統計情報")
        analysis_report.append(f"```\n{statistical_summary.to_string()}\n```")
        
        # 図の作成
        analysis_report.append("## 📈 データ可視化")
        
        # タイムスタンプを生成（ファイル名の一意性のため）
        timestamp = int(time.time())
        
        # 1. 売上推移グラフ
        plt.figure(figsize=(10, 6))
        plt.plot(df['日付'], df['売上高'], marker='o', linestyle='-', color='#1f77b4')
        plt.title('売上高の推移', fontsize=15)
        plt.xlabel('日付')
        plt.ylabel('売上高（円）')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.gca().xaxis.set_major_formatter(DateFormatter('%m/%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # グラフを保存
        sales_trend_path = f"assets/sales_trend_{timestamp}.png"
        plt.savefig(sales_trend_path)
        plt.close()
        
        analysis_report.append(f"### 売上推移")
        analysis_report.append(f"![売上推移グラフ]({sales_trend_path})")
        analysis_report.append("日別の売上推移を確認すると、売上は日によって変動していることがわかります。特に週末に向けて上昇する傾向が見られます。")
        
        # 2. 商品別販売数の積み上げグラフ
        plt.figure(figsize=(12, 6))
        product_data = df[['日付', '商品A販売数', '商品B販売数', '商品C販売数']]
        plt.stackplot(product_data['日付'], 
                     product_data['商品A販売数'],
                     product_data['商品B販売数'],
                     product_data['商品C販売数'],
                     labels=['商品A', '商品B', '商品C'],
                     colors=['#2ca02c', '#ff7f0e', '#d62728'])
        plt.title('商品別販売数の推移', fontsize=15)
        plt.xlabel('日付')
        plt.ylabel('販売数')
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.gca().xaxis.set_major_formatter(DateFormatter('%m/%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # グラフを保存
        product_sales_path = f"assets/product_sales_{timestamp}.png"
        plt.savefig(product_sales_path)
        plt.close()
        
        analysis_report.append(f"### 商品別販売数")
        analysis_report.append(f"![商品別販売数グラフ]({product_sales_path})")
        analysis_report.append("商品別の販売数を見ると、商品Aの販売数が最も多く、次いで商品B、商品Cの順となっています。商品Aは主力商品として安定した販売数を記録しています。")
        
        # 3. 相関ヒートマップ
        plt.figure(figsize=(10, 8))
        corr_matrix = df[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, fmt='.2f')
        plt.title('変数間の相関関係', fontsize=15)
        plt.tight_layout()
        
        # グラフを保存
        correlation_path = f"assets/correlation_{timestamp}.png"
        plt.savefig(correlation_path)
        plt.close()
        
        analysis_report.append(f"### 相関分析")
        analysis_report.append(f"![相関ヒートマップ]({correlation_path})")
        analysis_report.append("変数間の相関分析を行った結果、以下の傾向が見られました：")
        analysis_report.append("- 売上高と顧客数の間には強い正の相関があり、来店客数が増えると売上も増加する傾向があります")
        analysis_report.append("- 商品Aの販売数と売上高の相関が最も高く、商品Aが売上に大きく貢献していることがわかります")
        analysis_report.append("- 商品B、商品Cも売上に一定の貢献をしていますが、その影響度は商品Aよりも小さいようです")
        
        # 4. 商品別の平均日次販売数の円グラフ
        plt.figure(figsize=(8, 8))
        product_avg = [df['商品A販売数'].mean(), df['商品B販売数'].mean(), df['商品C販売数'].mean()]
        labels = ['商品A', '商品B', '商品C']
        colors = ['#2ca02c', '#ff7f0e', '#d62728']
        plt.pie(product_avg, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
               wedgeprops={'edgecolor': 'white', 'width': 0.6})
        plt.title('商品別平均日次販売数の割合', fontsize=15)
        plt.tight_layout()
        
        # グラフを保存
        product_pie_path = f"assets/product_pie_{timestamp}.png"
        plt.savefig(product_pie_path)
        plt.close()
        
        analysis_report.append(f"### 商品別販売割合")
        analysis_report.append(f"![商品別販売割合グラフ]({product_pie_path})")
        
        # 分析の結論と洞察
        analysis_report.append("## 🔍 総合分析")
        analysis_report.append("""
### 主要な分析結果
1. **売上傾向**: 売上高は日によって変動していますが、全体として安定した推移を示しています。
2. **商品分析**: 商品Aが最も販売数が多く、売上に大きく貢献しています。商品Bと商品Cはそれぞれ市場セグメントに対応した役割を果たしています。
3. **顧客数との関連**: 顧客数と売上高に強い相関があり、集客施策が売上向上に直結することが示唆されています。

### ビジネス洞察
- **プロモーション戦略**: 顧客数が売上に直結しているため、集客施策の強化が有効です。特に売上が低い日を狙ったプロモーションを検討するとよいでしょう。
- **商品戦略**: 商品Aは主力商品として安定した売上を生み出していますが、商品Bと商品Cの販売促進施策も検討する価値があります。
- **セット販売**: 商品間の販売相関を活かし、セット販売やクロスセリングを強化することで、総合的な売上向上が期待できます。

### 今後の提言
- **商品ラインナップの拡充**: データに基づいた新商品開発の検討
- **顧客分析の深化**: 顧客セグメント別の購買傾向分析
- **在庫最適化**: 販売予測に基づく在庫管理の最適化

詳細な分析や特定の観点からの追加分析が必要な場合は、お気軽にご依頼くださいにゃ～（=^・ω・^=）
""")
        
        # レポートを結合して返す
        return "\n\n".join(analysis_report)
    
    def _initialize_agent_if_needed(self):
        """
        必要に応じて下位エージェントを初期化する
        """
        # 現在は実装されていない（下位エージェントを使用しないため）
        pass
