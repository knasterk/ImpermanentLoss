from simulate import get_scenarios
from download import get_data
from simulate import simulate, get_best_strategy, scale_prices
from simulate import plot_impermanet_loss, save_results

DOWNLOAD_DATA = False
FEE_TIER = 0.0001

pair, t0, t1 = get_scenarios('MKR/ETH_all')
price_data, swap_data = get_data('MKR/ETH', download=DOWNLOAD_DATA)
sim_results, sim_performance, sim_data_collect, strategy = \
    simulate(price_data, swap_data, t0, t1, fee_tier=FEE_TIER)
best_results, values, best_id = get_best_strategy(sim_results, strategy)
fname = f'results/MKR-ETH_{t0.isoformat()[:10]}_{t1.isoformat()[:10]}.csv'
# fname = 'results/MKR-ETH_2021-10-23_2022-03-19.csv'
results = save_results(best_results, fname)
title = 'MKR/ETH -- all'
title = f'MKR/ETH -- {t0.isoformat()[:10]} to {t1.isoformat()[:10]}'
fig_fname = 'figs/MKR-ETH_all'
plot_impermanet_loss(results_fname=fname,
                     title=title,
                     quoteCurrency='ETH',
                     fig_fname=fig_fname)

pair, t0, t1 = get_scenarios('RAI/ETH_10x')
price_data, swap_data = get_data('RAI/ETH', download=DOWNLOAD_DATA)
price_data = scale_prices(price_data, t1, 4.5)
sim_results, sim_performance, sim_data_collect, strategy = \
    simulate(price_data, swap_data, t0, t1, fee_tier=FEE_TIER)
best_results, values, best_id = get_best_strategy(sim_results, strategy)
fname = 'results/RAI-ETH_10x.csv'
results = save_results(best_results, fname)
title = 'RAI/ETH -- 10x (scaled prices)'
fig_fname = 'figs/RAI-ETH_10x'
plot_impermanet_loss(results_fname=fname,
                     title=title,
                     quoteCurrency='ETH',
                     fig_fname=fig_fname)

pair, t0, t1 = get_scenarios('DAI/MKR_all')
price_data, swap_data = get_data('DAI/MKR', download=DOWNLOAD_DATA)
sim_results, sim_performance, sim_data_collect, strategy = \
    simulate(price_data, swap_data, t0, t1, fee_tier=FEE_TIER)
best_results, values, best_id = get_best_strategy(sim_results, strategy)
fname = f'results/DAI-MKR_{t0.isoformat()[:10]}_{t1.isoformat()[:10]}.csv'
# fname = 'results/DAI-MKR_2021-10-23_2022-03-19.csv'
results = save_results(best_results, fname)
title = 'DAI/MKR -- all'
title = f'DAI/MKR -- {t0.isoformat()[:10]} to {t1.isoformat()[:10]}'
fig_fname = 'figs/DAI-MKR_all'
plot_impermanet_loss(results_fname=fname,
                     title=title,
                     quoteCurrency='MKR',
                     fig_fname=fig_fname)

pair, t0, t1 = get_scenarios('RAI/ETH_2x')
price_data, swap_data = get_data('RAI/ETH', download=DOWNLOAD_DATA)
sim_results, sim_performance, sim_data_collect, strategy = \
    simulate(price_data, swap_data, t0, t1, fee_tier=FEE_TIER)
best_results, values, best_id = get_best_strategy(sim_results, strategy)
fname = 'results/RAI-ETH_2x.csv'
results = save_results(best_results, fname)
title = 'RAI/ETH -- 2x'
fig_fname = 'figs/RAI-ETH_2x'
plot_impermanet_loss(results_fname=fname,
                     title=title,
                     quoteCurrency='ETH',
                     fig_fname=fig_fname)

pair, t0, t1 = get_scenarios('RAI/ETH_2x_to_1x')
price_data, swap_data = get_data('RAI/ETH', download=DOWNLOAD_DATA)
sim_results, sim_performance, sim_data_collect, strategy = \
    simulate(price_data, swap_data, t0, t1, fee_tier=FEE_TIER)
best_results, values, best_id = get_best_strategy(sim_results, strategy)
fname = 'results/RAI-ETH_2x_to_1x.csv'
results = save_results(best_results, fname)
title = 'RAI/ETH -- 2x back to 1x'
fig_fname = 'figs/RAI-ETH_2x_to_1x'
plot_impermanet_loss(results_fname=fname,
                     title=title,
                     quoteCurrency='ETH',
                     fig_fname=fig_fname)

pair, t0, t1 = get_scenarios('RAI/ETH_all')
price_data, swap_data = get_data('RAI/ETH', download=DOWNLOAD_DATA)
sim_results, sim_performance, sim_data_collect, strategy = \
    simulate(price_data, swap_data, t0, t1, fee_tier=FEE_TIER)
best_results, values, best_id = get_best_strategy(sim_results, strategy)
fname = f'results/RAI-ETH_{t0.isoformat()[:10]}_{t1.isoformat()[:10]}.csv'
results = save_results(best_results, fname)
title = f'RAI/ETH -- {t0.isoformat()[:10]} to {t1.isoformat()[:10]}'
fig_fname = 'figs/RAI-ETH_all'
plot_impermanet_loss(results_fname=fname,
                     title=title,
                     quoteCurrency='ETH',
                     fig_fname=fig_fname)
