import random
from matplotlib import pyplot as plt
from tqdm import tqdm

# simulate a single game of the Saint Petersburg Paradox


def play_game(p, max_flips):
    # p is the probability of flipping heads
    # max_flips is the maximum number of coin flips
    money = 1
    flips = 0
    while random.random() < p and flips < max_flips:
        money *= 2
        flips += 1
    if flips == max_flips:
        return money
    else:
        return 0

# simulate many games of the Saint Petersburg Paradox and return the average winnings


def simulate_games(p, max_flips, n):
    total_return = 0
    for i in range(n):
        total_return += play_game(p, max_flips)
    return total_return / n


all_max_flips = [1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for num_simulations in [10, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]:
    # Print which simulation we're on
    print(f'Simulating {num_simulations} games...')

    # Simulate the game with two different coins for a variety of maximum flips
    expected_values_5050 = []
    expected_values_4951 = []
    expected_values_4852 = []
    for max_flips in tqdm(all_max_flips):

        # simulate the Saint Petersburg Paradox with a 50-50 coin
        ev_50 = simulate_games(0.5, 20, num_simulations)
        # print(ev_50)

        # simulate the Saint Petersburg Paradox with a 49-51 coin
        ev_51 = simulate_games(0.51, 20, num_simulations)
        # print(ev_51)

        # simulate the Saint Petersburg Paradox with a 48-52 coin
        ev_52 = simulate_games(0.52, 20, num_simulations)
        # print(ev_52)

        # Store the expected values
        expected_values_5050.append(ev_50)
        expected_values_4951.append(ev_51)
        expected_values_4852.append(ev_52)

    # Print the results, neatly formatted into a table so each column is aligned
    print('Maximum number of flips\tEV 50-50\tEV 49-51\tEV 48-52')
    for i in range(len(all_max_flips)):
        print(
            f'{all_max_flips[i]}\t\t\t{expected_values_5050[i]}\t\t{expected_values_4951[i]}\t\t{expected_values_4852[i]}')
    # Plot the expected values
    plt.clf()
    plt.plot(all_max_flips, expected_values_5050, label='50-50')
    plt.plot(all_max_flips, expected_values_4951, label='49-51')
    plt.plot(all_max_flips, expected_values_4852, label='48-52')
    plt.xlabel('Maximum number of flips')
    plt.ylabel('Expected value')
    plt.title('Expected value of the Saint Petersburg Paradox')
    plt.legend()
    # plt.show()

    # Save the plot
    plt.savefig(f'saint_petersburg_paradox_plot_{num_simulations}.png')

    # Save the data
    with open(f'saint_petersburg_paradox_data_{num_simulations}.txt', 'w') as f:
        f.write('Maximum number of flips,Expected value 50-50,Expected value 49-51,Expected value 48-52')
        for i in range(len(all_max_flips)):
            f.write(f'{all_max_flips[i]},{expected_values_5050[i]},{expected_values_4951[i]},{expected_values_4852[i]}')
