import datetime
import gym
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import animation
class DQAgent:
    def __init__(self, env):
        self.env = env
        num_states = (env.observation_space.high - env.observation_space.low) * np.array([10, 100])
        num_states = np.round(num_states, 0).astype(int) + 1
        self.Q = np.zeros((num_states[0], num_states[1],env.action_space.n))
        self.min = env.observation_space.low
    def save(self, path,start,end):
        np.save(path, self.Q)
        file = open('training_time.txt', 'w')
        file.write("start time is : "+str(start)+"\n"+"end time is : "+str(end)+"\n"+"total time is : "+str(end - start))
        file.close()
    def load(self, path):
        self.Q = np.load(path)
    def test(self):
      reward = 0
      env = self.env
      Q = self.Q
      obs = env.reset()
      done = False
      while done != True:
        state = self.get_state(obs)
        action = np.argmax(Q[state[0], state[1]])
        obs, r, done, info = env.step(action)
        reward +=r
        if done and obs[0] >= 0.5:
          break
      return reward
    def get_state(self,obs):
      return np.round((obs - self.min) * np.array([10, 100])).astype(int)
    def train(self, learning, discount, epsilon, minE, episodes):
        reduction = (epsilon - minE) / episodes
        env = self.env
        Q = self.Q
        start = datetime.now()
        for e in range(episodes) :
            done = False
            obs = env.reset()
            current = self.get_state(obs)
            while done != True:
                i,j = current[0],current[1]
                action = np.argmax(Q[i, j]) if np.random.random() > epsilon else np.random.randint(0, 3)
                obs, reward, done, info = env.step(action)
                next_state = self.get_state(obs)
                i_p,j_p = next_state[0],next_state[1]
                if done and obs[0] >= 0.5:
                    Q[i,j, action] = reward
                else:
                    Q[i,j, action] += learning * (reward + discount * np.max(Q[i_p,j_p]) -Q[i,j, action])
                current = next_state
                epsilon -= reduction
        env.close()
        self.Q = Q
        end = datetime.now()
        self.save("policy",start,end)
        return start,end
env = gym.make("MountainCar-v0")
agent = DQAgent(env)
start,end = agent.train(learning = 0.25, discount = 1, epsilon = 1, minE = 0, episodes = 50000  )
print("traning time : ",end - start)
agent.load("policy.npy")
rewards = []
for i in range(10000):
  rewards.append(agent.test())
np.save("reward_list_results", np.array(rewards))
array = np.load("reward_list_results.npy")
file = open('test_results.txt', 'w')
size = len(array)
s =sum(array >= -140)
res = "number of more than -140 from "+str(len(array))+" test : "+str(s)+" "+str(100*s/size)+"%\n"
s =sum(array >= -150)
res+="number of more than -150 from "+str(len(array))+" test :  "+str(s)+" "+str(100*s/size)+"%\n"
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.hist(array, bins=40, density=True, alpha=0.6, color='b')
plt.savefig("result_plot.png")
res+="rewards mean is : "+str(np.mean(array))+"\n"
res+="rewards std is : "+str(np.std(array))
file.write(res)
file.close()
print(res)

# save as gif
def save_frames_as_gif(frames, path='./', filename='animation.gif'):
    plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=72)
    patch = plt.imshow(frames[0])
    plt.axis('off')
    def animate(i):
        patch.set_data(frames[i])
    anim = animation.FuncAnimation(plt.gcf(), animate, frames = len(frames), interval=50)
    anim.save(path + filename, writer='Pillow', fps=60)
env = gym.make("MountainCar-v0")
agent = DQAgent(env)
agent.load("policy.npy")
def test_export_as_gif(name):
    frames = []
    Q = agent.Q
    obs = env.reset()
    for t in range(200):
        frames.append(env.render(mode="rgb_array"))
        state = agent.get_state(obs)
        action = np.argmax(Q[state[0], state[1]])
        obs, r, done, info = env.step(action)
        if done:
            break
    env.close()
    save_frames_as_gif(frames,filename = name)
for i in range(5):
    test_export_as_gif("animation"+str(i)+".gif")
