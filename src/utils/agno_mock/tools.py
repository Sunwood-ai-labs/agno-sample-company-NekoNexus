"""
agnoパッケージのツールモックの実装
"""

class DuckDuckGoTools:
    """
    DuckDuckGoツールのモック実装
    """
    
    def __init__(self):
        """
        DuckDuckGoツールの初期化
        """
        pass
    
    def search(self, query, max_results=5, search_type=None):
        """
        検索を実行するモック関数
        
        Args:
            query: 検索クエリ
            max_results: 最大結果数
            search_type: 検索タイプ
            
        Returns:
            検索結果のモックデータ
        """
        # 実際には検索を行わず、モック結果を返す
        return [
            {
                "title": f"検索結果 {i} for {query}",
                "url": f"https://example.com/result/{i}",
                "description": f"これは {query} に関する検索結果 {i} のモック説明です。"
            }
            for i in range(1, min(max_results + 1, 6))
        ]


class YFinanceTools:
    """
    YFinanceツールのモック実装
    """
    
    def __init__(self):
        """
        YFinanceツールの初期化
        """
        pass
    
    def get_stock_info(self, ticker):
        """
        株式情報を取得するモック関数
        
        Args:
            ticker: 株式シンボル
            
        Returns:
            株式情報のモックデータ
        """
        # 実際には株価を取得せず、モックデータを返す
        return {
            "ticker": ticker,
            "name": f"{ticker} Corporation",
            "price": 123.45,
            "change": 1.23,
            "change_percent": 1.01,
            "volume": 1000000,
            "market_cap": 1000000000,
            "pe_ratio": 15.5,
            "dividend_yield": 2.5
        }
    
    def get_historical_data(self, ticker, period="1mo"):
        """
        過去の株価データを取得するモック関数
        
        Args:
            ticker: 株式シンボル
            period: 期間
            
        Returns:
            過去データのモックリスト
        """
        # 実際にはデータを取得せず、モックデータを返す
        import datetime
        
        data = []
        today = datetime.datetime.now()
        
        for i in range(30):
            date = today - datetime.timedelta(days=i)
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": 120 + i * 0.5,
                "high": 125 + i * 0.5,
                "low": 118 + i * 0.5,
                "close": 122 + i * 0.5,
                "volume": 1000000 - i * 10000
            })
        
        return data
