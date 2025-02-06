use maze::Maze;
use maze::Agent;

fn main() {
    let mut maze = Maze::new();
    let mut agent = Agent::new(0.1, &mut maze, 0.25);
    let mut move_history = Vec::<i32>::new();
    for _ in 0..5000 {
        while !agent.env.is_done() {
            let action = agent.choose_action();
            agent.env.step(action);
            let state = agent.env.get_state();
            let reward = agent.env.get_reward();
            agent.update_state_history(state, reward);
            if agent.env.get_steps()> 10000 {
                agent.env.set_state([5,5]);
            }
        }
        agent.learn();
        move_history.push(agent.env.get_steps());
        agent.env.reset();
    }
    print!("move_history: {:?}", move_history);
}
