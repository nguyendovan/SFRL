import numpy as np
from game import mygym as gym
from training.ddqn_gw import DQNAgent
import cv2

EPISODES = 5000

if __name__ == "__main__":
    visual = True
    verbose = False
    env = gym.make(visual=visual, game='GridWorld')
    state_size = env.observation_space_shape
    action_size = len(env.action_space)
    agent = DQNAgent(state_size, action_size)
    # agent.load("training/save/gw-ddqn.h5")
    done = False
    batch_size = 32
    max_step = 500

    for e in range(EPISODES):
        print('Episode {}/{}'.format(e+1, EPISODES))
        state = env.reset()
        state = np.reshape(state, [1, state_size])

        for time in range(max_step):
            action = agent.act(state)
            next_state, reward, done, total_reward = env.step(action, agent)
            next_state = np.reshape(next_state, [1, state_size])
            if visual:
                cv2.imshow('state', next_state)
                cv2.waitKey(10)
            if verbose:
                if reward <= -1:
                    print('step reward: {}, total reward: {:2}, score: {}, e: {:.2}'.
                          format(reward, round(total_reward, 3), time, agent.epsilon))
            elif time == max_step - 1:
                print('total reward: {:2}, score: {}, e: {:.2}'.
                      format(round(total_reward, 3), time+1, agent.epsilon))
            state = np.reshape(state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                agent.update_target_model()
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e+1, EPISODES, time, agent.epsilon))
                break
            elif e % 10 == 0:
                agent.update_target_model()
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        if e % 10 == 0:
            agent.save("training/save/gw-ddqn.h5")
