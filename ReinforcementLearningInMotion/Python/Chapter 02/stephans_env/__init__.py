from gymnasium.envs.registration import register

register(
    id="stephans_env/MazeWorld-v0",
    entry_point="stephans_env.envs:MazeWorldEnv",
)
