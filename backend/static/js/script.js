$(document).ready(function() {
    $('#generate-chart').click(function() {
        let symbol = $('#symbol').val();
        let startDate = $('#start-date').val();
        let endDate = $('#end-date').val();
        let indicators = $('#indicators').val();

        $.ajax({
            url: '/chart',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                symbol: symbol,
                start_date: startDate,
                end_date: endDate,
                indicators: indicators
            }),
            success: function(data) {
                console.log(data); // Debug: log the response data

                let trace1 = {
                    x: data.map(row => row.Date),
                    close: data.map(row => row.Close),
                    decreasing: {line: {color: 'red'}},
                    high: data.map(row => row.High),
                    increasing: {line: {color: 'green'}},
                    low: data.map(row => row.Low),
                    open: data.map(row => row.Open),
                    type: 'candlestick',
                    xaxis: 'x',
                    yaxis: 'y'
                };

                let traces = [trace1];

                if (indicators.includes('ma')) {
                    let ma50 = {
                        x: data.map(row => row.Date),
                        y: data.map(row => row.MA50),
                        type: 'scatter',
                        mode: 'lines',
                        name: 'MA50'
                    };
                    traces.push(ma50);
                }

                if (indicators.includes('ema')) {
                    let ema50 = {
                        x: data.map(row => row.Date),
                        y: data.map(row => row.EMA50),
                        type: 'scatter',
                        mode: 'lines',
                        name: 'EMA50'
                    };
                    traces.push(ema50);
                }

                if (indicators.includes('bb')) {
                    let bb_upper = {
                        x: data.map(row => row.Date),
                        y: data.map(row => row.BB_Upper),
                        type: 'scatter',
                        mode: 'lines',
                        name: 'BB Upper'
                    };
                    let bb_lower = {
                        x: data.map(row => row.Date),
                        y: data.map(row => row.BB_Lower),
                        type: 'scatter',
                        mode: 'lines',
                        name: 'BB Lower'
                    };
                    traces.push(bb_upper, bb_lower);
                }

                if (indicators.includes('rsi')) {
                    let rsi = {
                        x: data.map(row => row.Date),
                        y: data.map(row => row.RSI),
                        type: 'scatter',
                        mode: 'lines',
                        name: 'RSI',
                        yaxis: 'y2'
                    };
                    traces.push(rsi);
                }

                let layout = {
                    title: `${symbol} Stock Chart`,
                    xaxis: {
                        rangeslider: {
                            visible: false
                        }
                    },
                    yaxis: {
                        title: 'Price'
                    },
                    yaxis2: {
                        title: 'RSI',
                        overlaying: 'y',
                        side: 'right'
                    }
                };

                Plotly.newPlot('chart', traces, layout);
            },
            error: function(xhr, status, error) {
                console.error("Error generating chart:", status, error);
            }
        });
    });

    $('#run-backtest').click(function() {
        let symbol = $('#symbol').val();
        let startDate = $('#start-date').val();
        let endDate = $('#end-date').val();
        let cash = 10000;  // example initial cash

        $.ajax({
            url: '/backtest',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                symbol: symbol,
                start_date: startDate,
                end_date: endDate,
                cash: cash
            }),
            success: function(data) {
                $('#backtest-results').html(`
                    <h2>Backtest Results</h2>
                    <p>Final Portfolio Value: ${data.final_value}</p>
                    <p>Sharpe Ratio: ${JSON.stringify(data.sharpe_ratio)}</p>
                    <p>Drawdown: ${JSON.stringify(data.drawdown)}</p>
                    <p>Trade Analyzer: ${JSON.stringify(data.trade_analyzer)}</p>
                `);
            },
            error: function(xhr, status, error) {
                console.error("Error running backtest:", status, error);
            }
        });
    });
});
