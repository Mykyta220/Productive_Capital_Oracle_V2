## Features

### 1. Independent Strategies
- **Doika Loop** – auto LONG ↔ SHORT reversals based on signal
- **Scalping** – auto-switching between `trend`, `level`, and `one_shot`
- **AI Selector** – decides LONG/SHORT using EMA, RSI, trend, sentiment, and LightGBM

### 2. AI & Analytics
- Daily training of LightGBM model from trades
- EMA20/50, RSI, Bollinger Bands, ATR
- Trend detection via regression
- Sentiment filter using CryptoPanic
- CoinMarketCap token filter (optional)

### 3. Real Binance Futures Execution
- Works with USDT or USDC (configurable)
- Dynamic leverage based on balance and Binance symbol limits
- minQty and stepSize enforced (no error 1111)
- Auto trailing stop after entry
- Adaptive TP/SL via ATR

### 4. Telegram Bot
- Commands: `/start`, `/stop`, `/status`, `/tokens`, `/train_all`, `/balance`
- Notifies every trade with strategy, token, TP/SL, leverage
- Sends daily PnL report at 23:59 UTC

### 5. Streamlit Dashboard
- Real-time trade table
- Cumulative PnL graph
- Filter by strategy and token

---

## Setup

```bash
git clone https://github.com/yourname/future_mikix.git
cd future_mikix
pip install -r requirements.txt
