#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NekoNexus メインアプリケーション
"""

import os
import streamlit as st
from dotenv import load_dotenv
from agents.manager.manager_cat import ManagerCat

# 環境変数の読み込み
load_dotenv()

# アプリケーションのタイトル設定
st.set_page_config(
    page_title="猫猫カンパニー NekoNexus",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    """
    メインアプリケーション実行関数
    """
    # ヘッダー画像表示
    st.image("assets/header.svg", use_column_width=True)
    
    # タイトルとサブタイトル
    st.title("🐱 猫猫カンパニー NekoNexus")
    st.subheader("AIエージェントによる自律的タスク処理システム")
    
    # サイドバー情報
    with st.sidebar:
        st.title("📋 システム情報")
        st.info("NekoNexusは猫猫カンパニーの業務効率化、顧客満足度向上、社内コミュニケーション円滑化のためのAIエージェントシステムです。")
        
        # デバッグモード切り替え
        debug_mode = st.checkbox("🔍 デバッグモード", value=False)
        
        # APIキー情報
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ OpenAI APIキー設定済み")
        else:
            st.error("❌ OpenAI APIキーが設定されていません")
            st.text_input("OpenAI APIキー", type="password", key="openai_api_key")
            if st.session_state.get("openai_api_key"):
                os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
                st.rerun()
                
        st.divider()
        st.markdown("© 2025 猫猫カンパニー")
    
    # メインエリア
    tab1, tab2, tab3 = st.tabs(["💬 チャット", "📊 ダッシュボード", "ℹ️ ヘルプ"])
    
    with tab1:
        # チャットインターフェース
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # 過去のメッセージ表示
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # マネージャー猫のインスタンス作成
        manager_cat = ManagerCat(debug_mode=debug_mode)
        
        # ユーザー入力
        if prompt := st.chat_input("マネージャー猫に質問してください..."):
            # ユーザーメッセージをチャット履歴に追加
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # ユーザーメッセージの表示
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # マネージャー猫からの回答を取得
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("マネージャー猫が考えています..."):
                    response = manager_cat.process_request(prompt)
                message_placeholder.markdown(response)
            
            # アシスタントメッセージをチャット履歴に追加
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with tab2:
        st.header("📊 システムダッシュボード")
        st.info("この機能は開発中です。将来のバージョンでリリース予定です。")
        
        # ダミーのダッシュボードデータ
        cols = st.columns(3)
        with cols[0]:
            st.metric(label="処理済みタスク", value="42", delta="↑4")
        with cols[1]:
            st.metric(label="平均応答時間", value="2.3秒", delta="-0.5秒")
        with cols[2]:
            st.metric(label="ユーザー満足度", value="95%", delta="↑2%")
            
    with tab3:
        st.header("ℹ️ ヘルプとドキュメント")
        st.markdown("""
        ### 使い方
        1. チャットタブでマネージャー猫に自然言語で質問やタスクを入力してください
        2. マネージャー猫が適切なサブエージェントにタスクを割り振り、処理します
        3. 結果が表示されるまでお待ちください
        
        ### 対応タスク例
        - 社内データの分析と可視化
        - 調査レポートの作成
        - スケジュール管理と調整
        - メール文面の作成
        - システム状態の監視
        
        ### よくある質問
        **Q: 応答が遅い場合はどうすればいいですか？**  
        A: タスクの複雑さによって処理時間が変わります。複雑なタスクは時間がかかることがあります。
        
        **Q: エラーが表示される場合は？**  
        A: APIキーが正しく設定されているか確認してください。また、複雑すぎるリクエストはサポートされていない場合があります。
        """)

if __name__ == "__main__":
    main()
