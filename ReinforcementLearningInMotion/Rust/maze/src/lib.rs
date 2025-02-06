use std::collections::hash_map::HashMap;
use rand::Rng;

pub struct Maze {
    width: usize,
    height: usize,
    cells: Vec<Vec<i32>>,
    state: [usize; 2],
    steps: i32,
    allowed_actions: HashMap<[usize; 2], Vec<char>>,
    target: [usize; 2],
}

impl Maze {
    pub fn new() -> Maze {
        Maze {
            width: 6,
            height: 6,
            cells: vec![vec![2,0,0,0,0,1],
                        vec![0,0,0,0,0,1],
                        vec![0,0,1,1,1,1],
                        vec![0,0,1,0,0,0],
                        vec![0,0,0,0,1,0],
                        vec![1,1,1,1,1,0]],
            state: [0, 0],
            target: [5, 5],
            steps: 0,
            allowed_actions: Maze::construct_allowed_actions(),
        }
    }

    fn construct_allowed_actions() -> HashMap<[usize; 2], Vec<char>> {
        let mut allowed_actions = HashMap::new();
        allowed_actions.insert([0, 0], vec!['D', 'R']);
        allowed_actions.insert([0, 1], vec!['D', 'R', 'L']);
        allowed_actions.insert([0, 2], vec!['D', 'R', 'L']);
        allowed_actions.insert([0, 3], vec!['D', 'R', 'L']);
        allowed_actions.insert([0, 4], vec!['D', 'L']);
        allowed_actions.insert([1, 0], vec!['D', 'R', 'U']);
        allowed_actions.insert([1, 1], vec!['D', 'R', 'L','U']);
        allowed_actions.insert([1, 2], vec!['R', 'L', 'U']);
        allowed_actions.insert([1, 3], vec!['R', 'L', 'U']);
        allowed_actions.insert([1, 4], vec!['L', 'U']);
        allowed_actions.insert([2, 0], vec!['D', 'R', 'U']);
        allowed_actions.insert([2, 1], vec!['D', 'U', 'L']);  
        allowed_actions.insert([3, 0], vec!['D', 'R', 'U']);
        allowed_actions.insert([3, 1], vec!['D', 'L', 'U']);
        allowed_actions.insert([3, 3], vec!['D', 'R']);
        allowed_actions.insert([3, 4], vec!['L', 'R']);
        allowed_actions.insert([3, 5], vec!['L', 'D']);
        allowed_actions.insert([4, 0], vec!['R', 'U']);
        allowed_actions.insert([4, 1], vec!['R', 'L', 'U']);
        allowed_actions.insert([4, 2], vec!['R', 'L']);
        allowed_actions.insert([4, 3], vec!['L', 'U']);
        allowed_actions.insert([4, 5], vec!['D', 'U']);
        allowed_actions.insert([5, 5], vec!['U']);
        allowed_actions
    }

    pub fn  step(&mut self, action: char) {
        let [y, x] = self.state;
        self.cells[y][x] = 0;
        if !self.allowed_actions[&self.state].contains(&action) {
            panic!("Invalid action");
        }
        match action {
            'U' => self.state = [y - 1, x],
            'D' => self.state = [y + 1, x],
            'L' => self.state = [y, x - 1],
            'R' => self.state = [y, x + 1],
            _ => panic!("Invalid action")
        }
        let [y, x] = self.state;
        self.cells[y][x] = 2;
        self.steps += 1;
    }

    pub fn is_done(&self) -> bool {
        self.state == self.target
    }

    pub fn print(&self) {
        for _ in 0..self.width {
            print!("-");
        }
        println!();
        for row in &self.cells {
            for cell in row {
                print!("{}", cell);
            }
            println!();
        }
        for _ in 0..self.width {
            print!("-");
        }
        println!();
    }

    pub fn get_allowed_actions(&self) -> &[char] {
        self.allowed_actions[&self.state].as_slice()
    }

    pub fn get_state(&self) -> [usize; 2] {
        self.state
    }

    pub fn get_reward(&self) -> f64 {
        if self.is_done() {
            0.0
        } else {
            -1.0
        }
    }
 
    pub fn set_state(&mut self, state: [usize; 2]) {
        self.state = state;
    }

    pub fn get_steps(&self) -> i32 {
        self.steps as i32
    }

    pub fn reset(&mut self) {
        self.state = [0, 0];
        self.steps = 0;
        self.cells = vec![vec![2,0,0,0,0,1],
                        vec![0,0,0,0,0,1],
                        vec![0,0,1,1,1,1],
                        vec![0,0,1,0,0,0],
                        vec![0,0,0,0,1,0],
                        vec![1,1,1,1,1,0]];
        self.state =  [0, 0];
        self.target =  [5, 5];
        self.allowed_actions = Maze::construct_allowed_actions();
    }
}

pub struct Agent<'a>{
    alpha: f64,
    g_table: HashMap<[usize; 2], f64>,
    state_history: Vec<([usize; 2], f64)>,
    random_action_prob: f64,
    pub env: &'a mut Maze
}

impl Agent<'_> {
    pub fn new(alpha: f64, env: &mut Maze, random_action_prob: f64) -> Agent {
        let mut agent = Agent {
            alpha,
            g_table: HashMap::new(),
            state_history: Vec::new(),
            random_action_prob,
            env: env,
        };
        agent.init_reward();
        agent
    }

    fn init_reward(&mut self) {
        for state in self.env.allowed_actions.keys() {
            self.g_table.insert(*state, rand::rng().random_range(-1.0..-0.1));
        }
    }

    pub fn choose_action(&self) -> char {
        let mut max_g = -10e15;
        let mut next_action = 'U';

        let random_n = rand::rng().random_range(0.0..1.0);

        if random_n < self.random_action_prob {
            let allowed_actions = self.env.get_allowed_actions();
            let random_index = rand::rng().random_range(0..allowed_actions.len());
            next_action = allowed_actions[random_index];
        } else {
            for action in self.env.get_allowed_actions() {
                let [y, x] = self.env.get_state();
                let point;
                match action {
                    'U' => point = [y - 1, x],
                    'D' => point = [y + 1, x],
                    'L' => point = [y, x - 1],
                    'R' => point = [y, x + 1],
                    _ => panic!("Invalid action")
                }
                let g = self.g_table[&point];
                if g > max_g {
                    max_g = g;
                    next_action = *action;
                }
            }
        }
        next_action
    }

    pub fn learn(&mut self) {
        let mut target = 0.0;
        for (prev, reward) in (self.state_history).iter().rev() {
            let g_table_prev_ref = self.g_table.get_mut(prev).unwrap(); 
            *g_table_prev_ref = *g_table_prev_ref +  self.alpha * (target - *g_table_prev_ref);
            target += reward;
        }
        println!("state_history: {:?}", self.state_history);
        self.state_history = Vec::<([usize; 2], f64)>::new();
        self.random_action_prob -= 10e-5;
    }

    pub fn update_state_history(&mut self, state: [usize; 2], reward: f64) {
        self.state_history.push((state, reward));
    }
}