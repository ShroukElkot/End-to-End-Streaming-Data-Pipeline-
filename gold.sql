-- Table 1: Market Data OHLCV
CREATE TABLE crypto_ohlcv (
    symbol VARCHAR(20),
    window_start DATETIME2,
    window_end DATETIME2,
    open_price DECIMAL(18,8),
    high_price DECIMAL(18,8),
    low_price DECIMAL(18,8),
    close_price DECIMAL(18,8),
    total_volume DECIMAL(18,8),
    total_trade_value DECIMAL(18,8),
    trade_count BIGINT,
    avg_price DECIMAL(18,8),
    price_stddev FLOAT,
    loaded_at DATETIME2
);

-- Table 2: Anomaly Alerts
CREATE TABLE crypto_anomalies (
    symbol VARCHAR(20),
    window_start DATETIME2,
    window_end DATETIME2,
    close_price DECIMAL(18,8),
    rolling_avg_30m DECIMAL(18,8),
    rolling_stddev_30m FLOAT,
    z_score DECIMAL(10,4),
    price_deviation_pct DECIMAL(10,4),
    volume_spike_ratio DECIMAL(10,2),
    anomaly_type VARCHAR(50),
    detection_time DATETIME2
);
