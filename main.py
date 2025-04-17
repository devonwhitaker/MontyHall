import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

trials = 1000
wins = 0
switch = True

door_choices_over_time = []
outcomes = []

trial_df = {'total_trials': 0,
            'wins': 0,
            'door_choices': [0,0,0],
            'car_positions': [0,0,0],
            'win_rate': []}

fig, c = plt.subplots(2, 2, figsize=(16,8))
fig.suptitle('Monty Hall Problem Visualized', fontsize=16)

c_stack = c[0, 0]
c_stack.set_title('Door Choices Over Time')

c_cars = c[0, 1]
car_bars = c_cars.bar(['Door 1', 'Door 2', 'Door 3'], trial_df['car_positions'])
c_cars.set_title('Car Placement')
c_cars.set_ylim(0, trials/2.5)

c_win_rate = c[1, 0]
wr_line, = c_win_rate.plot([], [], color='green')
c_win_rate.set_title("Win Rate Over Time")
c_win_rate.set_xlabel("Trials")
c_win_rate.set_ylabel("Win Rate")
c_win_rate.set_xlim(0, trials)
c_win_rate.set_ylim(0, 1)

c_outcomes = c[1, 1]
c_outcomes.set_title("Win/Loss Outcome by Trial")
c_outcomes.set_xlim(0, trials)
c_outcomes.set_ylim(0, 1)

def run_sim():
    doors = [1,2,3]
    car = random.choice(doors)
    choice = random.choice(doors)

    remaining_doors = [door for door in doors if door != choice and door != car]
    revealed_door = random.choice(remaining_doors)

    if switch:
        remaining_doors = [door for door in doors if door != choice and door != revealed_door]
        choice = remaining_doors[0]

    win = choice == car
    return choice, car, win

def update(frame):
    choice, car, win = run_sim()

    trial_df['total_trials'] += 1
    if win:
        trial_df['wins'] += 1

    outcomes.append(1 if win else 0)
    door_choices_over_time.append(trial_df['door_choices'].copy())

    trial_df['door_choices'][choice-1] += 1
    trial_df['car_positions'][car-1] += 1
    trial_df['win_rate'].append(trial_df['wins'] / trial_df['total_trials'])

    c_stack.clear()
    arr = np.array(door_choices_over_time).T
    c_stack.stackplot(range(len(door_choices_over_time)),
                      arr,
                      labels=["Door 1", "Door 2", "Door 3"],
                      colors=['#3498db', '#e67e22', '#9b59b6'])
    c_stack.legend(loc="upper left")
    c_stack.set_title("Door Choices Over Time")

    max_car_position = max(trial_df['car_positions'])
    c_cars.set_ylim(0, max_car_position * 1.2) 
    for i, bar in enumerate(car_bars):
        bar.set_height(trial_df['car_positions'][i])

    c_outcomes.clear()
    colors = ['green' if o == 1 else 'red' for o in outcomes]
    c_outcomes.scatter(range(len(outcomes)), [0.5]*len(outcomes), c=colors, s=100)
    c_outcomes.set_title("Win/Loss Outcome by Trial")
    c_outcomes.set_xlim(0, frame)
    c_outcomes.set_ylim(0, 1)
    c_outcomes.axis('off')

    c_win_rate.set_xlim(0, frame)
    c_win_rate.set_ylim(0, 1)
    wr_line.set_data(range(len(trial_df['win_rate'])), trial_df['win_rate'])

    return  list(car_bars) + [wr_line]

animate = FuncAnimation(fig, update, frames=trials, interval=1, blit=False, repeat=False)

plt.tight_layout()
writer = PillowWriter(fps=250)
animate.save("C:/Users/devon/Desktop/monty_hall_simulation.gif", writer=writer)
plt.show()
_ = animate

