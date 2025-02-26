#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日本語フォント設定ユーティリティモジュール
matplotlibなどで日本語を正しく表示するためのヘルパー関数を提供
"""

import os
import platform
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import subprocess
import warnings

def setup_japanese_fonts():
    """
    日本語フォントの設定を行う
    
    Returns:
        bool: フォント設定が成功したかどうか
    """
    # 使用可能なフォントをチェック
    font_found = False
    
    # システムに応じたフォントディレクトリの設定
    system = platform.system()
    
    # IPAフォントのインストールパスを確認
    font_paths = []
    if system == 'Linux':
        # Linuxの標準的なIPAフォントの場所
        font_paths = [
            '/usr/share/fonts/opentype/ipafont-gothic',
            '/usr/share/fonts/opentype/ipafont-mincho',
            '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
            '/usr/share/fonts/truetype/fonts-japanese-mincho.ttf',
            '/usr/share/fonts/truetype/ipafont'
        ]
    elif system == 'Windows':
        # Windowsの標準的なフォント場所
        font_paths = [
            os.path.join(os.environ['WINDIR'], 'Fonts')
        ]
    elif system == 'Darwin':  # macOS
        # macOSの標準的なフォント場所
        font_paths = [
            '/System/Library/Fonts',
            '/Library/Fonts',
            os.path.expanduser('~/Library/Fonts')
        ]
    
    # フォントキャッシュの更新
    for font_path in font_paths:
        if os.path.exists(font_path):
            # ディレクトリの場合
            if os.path.isdir(font_path):
                for font_file in os.listdir(font_path):
                    try:
                        if font_file.endswith('.ttf') or font_file.endswith('.ttc') or font_file.endswith('.otf'):
                            full_path = os.path.join(font_path, font_file)
                            fm.fontManager.addfont(full_path)
                    except Exception as e:
                        warnings.warn(f"フォント '{font_file}' の追加中にエラーが発生しました: {e}")
            # 単一ファイルの場合
            else:
                try:
                    fm.fontManager.addfont(font_path)
                except Exception as e:
                    warnings.warn(f"フォント '{font_path}' の追加中にエラーが発生しました: {e}")
    
    # フォントマネージャーのキャッシュを再構築
    # 旧バージョン: fm._rebuild()
    # 最新バージョンでは不要、fontManager.addfontで自動的にキャッシュが更新される
    
    # 日本語フォントの候補
    font_candidates = [
        'IPAGothic', 'IPAexGothic', 'IPAPGothic', 'IPAMincho', 'IPAexMincho', 
        'Noto Sans CJK JP', 'MS Gothic', 'VL Gothic', 'Meiryo', 'TakaoGothic',
        'Hiragino Sans GB', 'Hiragino Kaku Gothic Pro'
    ]
    
    # 利用可能なフォントを探す
    for font in font_candidates:
        if any(f.name == font for f in fm.fontManager.ttflist):
            matplotlib.rcParams['font.family'] = 'sans-serif'
            matplotlib.rcParams['font.sans-serif'] = [font, 'DejaVu Sans', 'Bitstream Vera Sans', 'Arial Unicode MS']
            print(f"INFO: 日本語フォント '{font}' を使用します。")
            font_found = True
            
            # テスト文字列でフォントが機能するか確認
            try:
                fig = plt.figure(figsize=(1, 1))
                plt.text(0.5, 0.5, '日本語テスト')
                plt.close(fig)
            except Exception as e:
                print(f"WARNING: フォント '{font}' でのテスト中にエラーが発生しました: {e}")
                font_found = False
                continue
                
            break
    
    # 日本語フォントが見つからない場合はデフォルト設定
    if not font_found:
        print("WARNING: 適切な日本語フォントが見つかりません。デフォルトフォントを使用します。")
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Bitstream Vera Sans', 'Arial Unicode MS']
    
    # バックエンド設定
    matplotlib.use('Agg')
    
    return font_found

def check_japanese_fonts():
    """
    利用可能な日本語フォントの一覧を表示
    
    Returns:
        list: 利用可能な日本語フォントのリスト
    """
    # フォントマネージャーのキャッシュを再構築
    # 旧バージョン: fm._rebuild()
    # 最新バージョンでは不要、fontManager.addfontで自動的にキャッシュが更新される
    
    # 日本語フォントの検索パターン
    japanese_patterns = [
        'IPA', 'Meiryo', 'MS Gothic', 'MS PGothic', 'MS Mincho', 'MS PMincho',
        'Noto Sans CJK JP', 'Hiragino', 'VL Gothic', 'Takao', '游ゴシック', '游明朝',
        'Yu Gothic', 'Yu Mincho'
    ]
    
    # 利用可能なフォントをフィルタリング
    available_fonts = []
    for font in fm.fontManager.ttflist:
        for pattern in japanese_patterns:
            if pattern.lower() in font.name.lower():
                available_fonts.append(font.name)
                break
    
    # 重複を削除してソート
    available_fonts = sorted(list(set(available_fonts)))
    
    print(f"利用可能な日本語フォント ({len(available_fonts)}個):")
    for font in available_fonts:
        print(f" - {font}")
    
    return available_fonts

if __name__ == "__main__":
    # このファイルが直接実行された場合、日本語フォントの設定とチェックを行う
    setup_japanese_fonts()
    check_japanese_fonts()
