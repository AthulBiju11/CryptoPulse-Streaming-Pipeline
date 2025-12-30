-- Query 1: Price Trend (Last 1 Hour)
-- Visualization: Line Chart (X: window_end, Y: avg_price, Group: symbol)
SELECT 
    window_end, 
    symbol, 
    avg_price
FROM cryptopulse_catalog.gold.dm_crypto_price_stats
WHERE window_end >= current_timestamp() - INTERVAL 1 HOUR
ORDER BY window_end ASC;

-- Query 2: Recent Market Alerts
-- Visualization: Table
SELECT 
    detected_at, 
    symbol, 
    alert_type, 
    price_change_pct, 
    start_price, 
    end_price
FROM cryptopulse_catalog.gold.dm_market_alerts
ORDER BY detected_at DESC
LIMIT 20;

-- Query 3: Trade Volume Analysis (Last 1 Hour)
-- Visualization: Bar Chart (X: window_end, Y: total_trade_volume, Group: symbol)
SELECT 
    window_end, 
    symbol, 
    total_trade_volume
FROM cryptopulse_catalog.gold.dm_crypto_price_stats
WHERE window_end >= current_timestamp() - INTERVAL 1 HOUR
ORDER BY window_end ASC;
