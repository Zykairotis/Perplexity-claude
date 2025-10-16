# Comprehensive Python Crypto Trading Bot

Here's a comprehensive Python crypto trading bot implementation using modern best practices for 2025:

## Basic Trading Bot Setup

```python
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CryptoTradingBot:
    def __init__(self, exchange_id='binance', api_key=None, api_secret=None, 
                 symbol='BTC/USDT', timeframe='1h', paper_trading=True):
        """
        Initialize crypto trading bot
        
        Args:
            exchange_id: Exchange name (binance, coinbase, kraken, etc.)
            api_key: Your API key
            api_secret: Your API secret
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candlestick timeframe ('1m', '5m', '1h', '1d')
            paper_trading: If True, simulates trades without real execution
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.paper_trading = paper_trading
        
        # Initialize exchange
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,  # Respect rate limits
            'options': {
                'defaultType': 'future'  # 'spot' or 'future'
            }
        })
        
        if paper_trading:
            self.exchange.set_sandbox_mode(True)  # Use testnet
            logger.info("Running in PAPER TRADING mode")
        
        self.position = None
        self.balance = self.get_balance()
    
    def get_balance(self):
        """Fetch account balance"""
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return None
    
    def fetch_ohlcv(self, limit=100):
        """Fetch historical OHLCV data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                self.symbol,
                self.timeframe,
                limit=limit
            )
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"Error fetching OHLCV: {e}")
            return None
    
    def calculate_indicators(self, df):
        """Calculate technical indicators"""
        # Simple Moving Averages
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['signal']
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # ATR for volatility-based position sizing
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['atr'] = true_range.rolling(14).mean()
        
        return df
    
    def generate_signal(self, df):
        """
        Generate trading signals based on strategy
        
        Returns:
            'BUY', 'SELL', or 'HOLD'
        """
        if len(df) < 50:
            return 'HOLD'
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Strategy: EMA crossover + RSI confirmation
        buy_conditions = [
            latest['ema_12'] > latest['ema_26'],  # Short EMA above long EMA
            prev['ema_12'] <= prev['ema_26'],  # Crossover just happened
            latest['rsi'] > 30 and latest['rsi'] < 70,  # Not overbought/oversold
            latest['close'] > latest['sma_20']  # Price above support
        ]
        
        sell_conditions = [
            latest['ema_12'] < latest['ema_26'],
            prev['ema_12'] >= prev['ema_26'],
            latest['rsi'] > 30,  # Avoid selling in oversold
        ]
        
        if all(buy_conditions):
            return 'BUY'
        elif all(sell_conditions) or (latest['rsi'] > 80):  # Aggressive sell on extreme overbought
            return 'SELL'
        
        return 'HOLD'
    
    def calculate_position_size(self, df, risk_percent=0.02):
        """
        Calculate position size based on ATR and risk percentage
        
        Args:
            df: DataFrame with price data and indicators
            risk_percent: Percentage of capital to risk per trade (default 2%)
        """
        latest = df.iloc[-1]
        current_price = latest['close']
        atr = latest['atr']
        
        # Get available balance
        base_currency = self.symbol.split('/')[1]  # e.g., 'USDT' from 'BTC/USDT'
        available_balance = self.balance['free'].get(base_currency, 0)
        
        # Calculate position size based on ATR
        # Risk amount = account balance * risk percentage
        risk_amount = available_balance * risk_percent
        
        # Position size = risk amount / (ATR * multiplier)
        # Using 2x ATR as stop loss distance
        stop_distance = atr * 2
        position_size = risk_amount / stop_distance
        
        # Convert to actual units
        units = position_size / current_price
        return units
    
    def place_order(self, order_type, side, amount, price=None):
        """
        Place an order
        
        Args:
            order_type: 'market' or 'limit'
            side: 'buy' or 'sell'
            amount: Amount in base currency
            price: Limit price (only for limit orders)
        """
        try:
            if self.paper_trading:
                logger.info(f"PAPER TRADE: {side.upper()} {amount} {self.symbol} at {order_type}")
                return {'id': 'paper_trade', 'status': 'closed'}
            
            if order_type == 'market':
                order = self.exchange.create_market_order(
                    self.symbol,
                    side,
                    amount
                )
            elif order_type == 'limit':
                order = self.exchange.create_limit_order(
                    self.symbol,
                    side,
                    amount,
                    price
                )
            
            logger.info(f"Order placed: {order}")
            return order
        
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    def set_stop_loss_take_profit(self, entry_price, side, atr_multiplier=2, reward_ratio=2):
        """
        Set stop loss and take profit levels
        
        Args:
            entry_price: Entry price of the position
            side: 'buy' or 'sell'
            atr_multiplier: ATR multiplier for stop loss
            reward_ratio: Risk/reward ratio for take profit
        """
        df = self.fetch_ohlcv()
        df = self.calculate_indicators(df)
        atr = df.iloc[-1]['atr']
        
        if side == 'buy':
            stop_loss = entry_price - (atr * atr_multiplier)
            take_profit = entry_price + (atr * atr_multiplier * reward_ratio)
        else:
            stop_loss = entry_price + (atr * atr_multiplier)
            take_profit = entry_price - (atr * atr_multiplier * reward_ratio)
        
        logger.info(f"Stop Loss: {stop_loss:.2f}, Take Profit: {take_profit:.2f}")
        return stop_loss, take_profit
    
    def run(self, check_interval=60):
        """
        Main trading loop
        
        Args:
            check_interval: Seconds between each check
        """
        logger.info(f"Starting trading bot for {self.symbol}")
        logger.info(f"Timeframe: {self.timeframe}, Check interval: {check_interval}s")
        
        while True:
            try:
                # Fetch data
                df = self.fetch_ohlcv()
                if df is None:
                    time.sleep(check_interval)
                    continue
                
                # Calculate indicators
                df = self.calculate_indicators(df)
                
                # Generate signal
                signal = self.generate_signal(df)
                current_price = df.iloc[-1]['close']
                
                logger.info(f"Price: {current_price:.2f} | Signal: {signal} | RSI: {df.iloc[-1]['rsi']:.2f}")
                
                # Execute trades based on signal
                if signal == 'BUY' and self.position != 'long':
                    amount = self.calculate_position_size(df)
                    order = self.place_order('market', 'buy', amount)
                    if order:
                        self.position = 'long'
                        self.set_stop_loss_take_profit(current_price, 'buy')
                
                elif signal == 'SELL' and self.position == 'long':
                    # Close position
                    order = self.place_order('market', 'sell', amount)
                    if order:
                        self.position = None
                
                time.sleep(check_interval)
            
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(check_interval)


# Usage example
if __name__ == "__main__":
    # Initialize bot (paper trading mode)
    bot = CryptoTradingBot(
        exchange_id='binance',
        api_key='YOUR_API_KEY',
        api_secret='YOUR_API_SECRET',
        symbol='BTC/USDT',
        timeframe='1h',
        paper_trading=True  # Set False for live trading
    )
    
    # Run the bot
    bot.run(check_interval=300)  # Check every 5 minutes
```

## Advanced Features Implementation

```python
# backtesting.py
import backtrader as bt

class CryptoStrategy(bt.Strategy):
    params = (
        ('ema_short', 12),
        ('ema_long', 26),
        ('rsi_period', 14),
        ('risk_percent', 0.02),
    )
    
    def __init__(self):
        self.ema_short = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=self.params.ema_short
        )
        self.ema_long = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=self.params.ema_long
        )
```tors.ExponentialMovingAverage( self.data.close, period=self.params.ema_long ) self.rsi = bt.indicators.RSI(period=self.params.rsi_period) self.crossover = bt.indicators.CrossOver(self.ema_short, self.ema_long) def next(self): if not self.position: if self.crossover > 0 and 30 < self.rsi < 70: size = self.broker.getcash() * self.params.risk_percent / self.data.close[0] self.buy(size=size) else: if self.crossover < 0 or self.rsi > 80: self.close() def run_backtest(symbol='BTC/USDT', start_date='2024-01-01'): cerebro = bt.Cerebro() cerebro.addstrategy(CryptoStrategy) # Add data feed (you would fetch this using ccxt) # data = bt.feeds.PandasData(dataname=your_dataframe) # cerebro.adddata(data) cerebro.broker.setcash(10000.0) cerebro.broker.setcommission(commission=0.001) # 0.1% commission print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}') cerebro.run() print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}') cerebro.plot() ``` ## Key Features This implementation includes **essential crypto trading components**:[1][2] The bot uses **CCXT library** which supports 100+ cryptocurrency exchanges including Binance, Coinbase, Kraken, and others with a unified API interface. The code implements **EMA crossover strategy** with RSI confirmation, **ATR-based position sizing** for risk management (default 2% risk per trade), and **automatic stop-loss and take-profit** calculations.[2][3][1] ### Risk Management Position sizing is calculated using the **ATR (Average True Range)** indicator to adjust for market volatility. The bot uses a 2:1 reward-to-risk ratio by default, and includes rate limiting to respect exchange API limits.[3][2] ### Setup Requirements Install dependencies with: ```bash pip install ccxt pandas numpy python-dateutil ``` For backtesting, also install: ```bash pip install backtrader matplotlib ``` ### Configuration Replace `YOUR_API_KEY` and `YOUR_API_SECRET` with your exchange credentials. Set `paper_trading=True` for sandbox/testnet trading, and adjust `risk_percent`, `timeframe`, and strategy parameters based on your risk tolerance.[1][2] ### Popular Alternatives For production use, consider established frameworks like **Freqtrade** (full-featured bot with Telegram control and machine learning support) or **Jesse** (self-hosted framework with advanced backtesting). Both offer more extensive features than a custom implementation.[4][5][6][7]