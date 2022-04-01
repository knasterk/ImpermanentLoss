import pandas as pd
import numpy as np
import AutoRegressiveStrategy as ARS
import ActiveStrategyFramework as ASF
import itertools
import importlib
import matplotlib.pyplot as plt


def get_scenarios(scenario):
    """
    """
    if scenario == 'DAI/MKR_all':
        pair = 'DAI/MKR'
        t0 = pd.to_datetime('2021-10-23 14:07:12+00:00', utc=True)
        t1 = pd.to_datetime('2022-03-19 16:18:18+00:00', utc=True)

    if scenario == 'DAI/MKR_2x':
        pair = 'DAI/MKR'
        t0 = pd.to_datetime('2021-06-27 06:19:00+0000', utc=True)
        t1 = pd.to_datetime('2021-08-25 13:58:00+0000', utc=True)

    if scenario == 'DAI/MKR_10x':
        pair = 'DAI/MKR'
        t0 = pd.to_datetime('2021-06-27 06:19:00+0000', utc=True)
        t1 = pd.to_datetime('2021-08-25 13:58:00+0000', utc=True)

    elif scenario == 'RAI/ETH_2x':
        pair = 'RAI/ETH'
        t0 = pd.to_datetime('2021-06-21 15:36:00+00:00', utc=True)
        t1 = pd.to_datetime('2021-11-19 02:55:00+00:00', utc=True)
        # t0 = pd.to_datetime('2021-05-14 22:44:00+00:00', utc=True)
        # t1 = pd.to_datetime('2021-07-25 18:02:00+00:00', utc=True)

    elif scenario == 'RAI/ETH_10x':
        pair = 'RAI/ETH'
        t0 = pd.to_datetime('2021-07-20 05:02:00+00:00', utc=True)
        t1 = pd.to_datetime('2021-11-12 05:39:00+00:00', utc=True)

    elif scenario == 'RAI/ETH_2x_to_1x':
        pair = 'RAI/ETH'
        t0 = pd.to_datetime('2021-05-25 12:19:00+00:00', utc=True)
        t1 = pd.to_datetime('2022-02-24 16:13:00+00:00', utc=True)

    elif scenario == 'RAI/ETH_all':
        pair = 'RAI/ETH'
        t0 = pd.to_datetime('2021-05-05 19:58:42+00:00', utc=True)
        t1 = pd.to_datetime('2022-03-23 22:25:00+00:00', utc=True)

    elif scenario == 'MKR/ETH_all':
        pair = 'MKR/ETH'
        t0 = pd.to_datetime('2021-05-06 00:59:25+00:00', utc=True)
        t1 = pd.to_datetime('2022-03-28 14:20:03+00:00', utc=True)

    elif scenario == 'DAI/ETH_all':
        pair = 'DAI/ETH'
        t0 = pd.to_datetime('2021-05-06 00:59:25+00:00', utc=True)
        t1 = pd.to_datetime('2022-03-28 14:20:03+00:00', utc=True)

    return pair, t0, t1


def scale_prices(price_data, t, scale):
    """
    """
    p = price_data['quotePrice'].loc[t]
    if type(p) == pd.core.series.Series:
        p = p[0]
    price_data['quotePrice'] = (price_data['quotePrice'] - p) * scale + p

    return price_data


def simulate(price_data, swap_data, t0, t1,
             fee_tier=0.003, decimals0=18, decimals1=18):
    """
    Run Auto Regressive Strategy

    # Select date ranges for strategy simulation
    t0 = pd.to_datetime('2021-09-01 00:00PM', utc=True)
    t1 = pd.to_datetime('2021-12-10 00:00PM', utc=True)
    """
    z_score_cutoff = 5
    window_size = 60

    # forecast returns at a daily frequency
    STAT_MODEL_FREQ = 'H'
    # Data for strategy simulation cleaning
    STRATEGY_FREQ = 'H'
    simulate_data_filtered = ASF.aggregate_price_data(price_data,
                                                      STRATEGY_FREQ)
    simulate_data_filtered_roll = simulate_data_filtered.quotePrice.rolling(window=window_size)
    simulate_data_filtered['roll_median'] = simulate_data_filtered_roll.median()
    roll_dev = np.abs(simulate_data_filtered.quotePrice - simulate_data_filtered.roll_median)
    simulate_data_filtered['median_abs_dev'] = 1.4826 * roll_dev.rolling(window=window_size).median()
    outlier_indices = np.abs(simulate_data_filtered.quotePrice - simulate_data_filtered.roll_median) >= z_score_cutoff*simulate_data_filtered['median_abs_dev']
    simulate_data_price = simulate_data_filtered[~outlier_indices]['quotePrice'][t0: t1]

    # Data for strategy simulation.
    # We can use aggregate_price_data to analyze the strategy at a coarser
    # STRATEGY_FREQUENCY in minutes
    simulate_data_price = simulate_data_filtered['quotePrice'][t0: t1]

    # Initial Position Details
    INITIAL_TOKEN_0 = 100000
    INITIAL_TOKEN_1 = INITIAL_TOKEN_0 * simulate_data_price[0]

    importlib.reload(ASF)
    importlib.reload(ARS)

    swap_data['virtual_liquidity'] = swap_data['VIRTUAL_LIQUIDITY_ADJUSTED']*(10**((decimals1  + decimals0)/2))
    swap_data['traded_in'] = swap_data.apply(lambda x: -x['amount0'] if (x['amount0'] < 0) else -x['amount1'], axis=1).astype(float)
    swap_data['traded_out'] = swap_data.apply(lambda x:  x['amount0'] if (x['amount0'] > 0) else x['amount1'], axis=1).astype(float)

    # Strategy Parameters
    alpha_range = [.50, .75, .95]
    tau_range = [.25, 0.75]
    vol_range = [0.85, .95]
    sim_performance = []
    sim_results = []
    sim_data_collect = []

    for alpha, tau, vol in list(itertools.product(alpha_range, tau_range, vol_range)):
        print(alpha, tau, vol)
        strategy = ARS.AutoRegressiveStrategy(price_data,
                                              alpha,
                                              tau,
                                              vol,
                                              data_frequency=STAT_MODEL_FREQ,
                                              return_forecast_cutoff=.5)
        simulated_strategy = ASF.simulate_strategy(simulate_data_price,
                                                   swap_data,
                                                   strategy,
                                                   INITIAL_TOKEN_0,
                                                   INITIAL_TOKEN_1,
                                                   fee_tier,
                                                   decimals0,
                                                   decimals1)
        sim_data = ASF.generate_simulation_series(simulated_strategy, strategy)
        strat_result = ASF.analyze_strategy(sim_data, frequency=STRATEGY_FREQ)
        strat_result['alpha_param'] = alpha
        strat_result['tau_param'] = tau
        strat_result['volatility_param'] = vol
        sim_results.append(simulated_strategy)
        sim_performance.append(strat_result)
        sim_data_collect.append(sim_data)

    return sim_results, sim_performance, sim_data_collect, strategy


def get_best_strategy(sim_results, strategy):
    """
    data_strategy = pd.DataFrame([strategy.dict_components(i) for i in resulting_strat])
    """

    # First compare all simulations based on value of position in USD
    values = np.zeros((len(sim_results), 3))
    for i, sim_result in enumerate(sim_results):
        result_data = ASF.generate_simulation_series(sim_result, strategy)
        values[i, 0] = float(result_data['value_position_usd'].iloc[-1])
        values[i, 1] = result_data['value_position_usd'].max()
        values[i, 2] = result_data['value_position_usd'].mean()

    best_id = np.argmax(values[:, 0])
    best_results = ASF.generate_simulation_series(sim_results[best_id],
                                                  strategy)

    return best_results, values, best_id


def save_results(results, fname):
    """
    """
    results['IL'] = (results['value_position_usd'] - results['value_hold_usd']) / results['value_hold_usd']

    results.to_csv(fname)

    return results


def plot_impermanet_loss(results_fname,
                         title,
                         quoteCurrency,
                         fig_fname,
                         figsize=(10, 5.5)):
    """
    """
    results = pd.read_csv(results_fname)
    results['time'] = pd.to_datetime(results['time'], utc=True)
    results.set_index('time', inplace=True)

    fig = plt.figure(figsize=figsize)

    # ax1 = fig.add_axes((0.07, 0.12, 0.84, 0.8))
    ax1 = fig.add_axes((0.11, 0.16, 0.77, 0.72))
    (results['IL'] * 100).plot(ax=ax1, label='Impermanent Loss')
    ax1.set_ylabel('Impermanent Loss (%)')
    ax1.set_title(title)
    ax1.set_xlabel('Date')
    ax1.legend(loc='upper left')
    ylim = ax1.get_ylim()
    xlim = ax1.get_xlim()
    plt.grid()
    ax1.set_ylim(ylim)
    ax1.set_xlim(xlim)

    label = f"{title.split('/')[0]} price in {quoteCurrency}"

    ax2 = ax1.twinx()
    results['price'].plot(ax=ax2, color='tab:orange', label=label)
    # ax2.plot(0, 0, color='tab:blue', label='IL')
    # ax2.plot(0, 0, color='tab:orange', label='price')
    ax2.set_ylabel(f'Price ({quoteCurrency})')
    ax2.legend(loc='upper right')
    xlim = ax2.get_xlim()

    ax1.spines['left'].set_position(('outward', 7))
    ax1.yaxis.set_ticks_position('left')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.spines['right'].set_position(('outward', 7))
    ax2.yaxis.set_ticks_position('right')
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    ax2.set_xlim(xlim)

    fig.savefig(f'{fig_fname}.png')

    if 'RAI' in title:
        price_usd = 3. / results['price']
        ylabel = f'USD per {quoteCurrency}'
        label = f'{quoteCurrency} price in USD (RAI/3)'
        if '10x' in title:
            lo = 1643.2073557898657
            d = 9.836015100312919 * lo - lo
            price_usd = lo + d * ((price_usd - price_usd.min()) /
                                  price_usd.max())
    elif 'DAI' in title:
        price_usd = 1. / results['price']
        ylabel = f'USD (DAI) per {quoteCurrency}'
        label = f'{quoteCurrency} price in USD (DAI)'
    else:
        return

    # fig = plt.figure(figsize=(12, 6))
    fig = plt.figure(figsize=figsize)

    # ax1 = fig.add_axes((0.07, 0.12, 0.84, 0.8))
    ax1 = fig.add_axes((0.11, 0.16, 0.76, 0.75))
    (results['IL'] * 100).plot(ax=ax1, label='Impermanent Loss')
    ax1.set_ylabel('Impermanent Loss (%)')
    ax1.set_title(title)
    ax1.set_xlabel('Date')
    ax1.legend(loc='upper left')
    plt.grid()

    ax2 = ax1.twinx()
    price_usd.plot(ax=ax2, color='tab:orange', label=label)
    # ax2.plot(0, 0, color='tab:blue', label='IL')
    # ax2.plot(0, 0, color='tab:orange', label='price')
    ax2.set_ylabel(ylabel)
    ax2.legend(loc='upper right')

    ax1.spines['left'].set_position(('outward', 7))
    ax1.yaxis.set_ticks_position('left')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.spines['right'].set_position(('outward', 7))
    ax2.yaxis.set_ticks_position('right')
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    fig.savefig(f'{fig_fname}_USD.png')
