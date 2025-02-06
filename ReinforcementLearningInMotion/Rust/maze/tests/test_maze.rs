use Maze;

#[test]
fn test_maze() {
    let mut maze = Maze::new();
    assert_eq!(maze.get_state(), [0, 0]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'R']);
    maze.step('D');
    assert_eq!(maze.get_state(), [1, 0]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'R']);
    maze.step('D');
    assert_eq!(maze.get_state(), [2, 0]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'R', 'U']);
    maze.step('R');
    assert_eq!(maze.get_state(), [2, 1]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'R', 'L']);
    maze.step('R');
    assert_eq!(maze.get_state(), [2, 2]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'R', 'L']);
    maze.step('R');
    assert_eq!(maze.get_state(), [2, 3]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'R', 'L']);
    maze.step('R');
    assert_eq!(maze.get_state(), [2, 4]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'L']);
    maze.step('D');
    assert_eq!(maze.get_state(), [3, 4]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'L', 'U']);
    maze.step('D');
    assert_eq!(maze.get_state(), [4, 4]);
    assert_eq!(maze.get_allowed_actions(), ['R', 'L', 'U']);
    maze.step('R');
    assert_eq!(maze.get_state(), [4, 5]);
    assert_eq!(maze.get_allowed_actions(), ['D', 'L']);
    maze.step('D');
    assert_eq!(maze.get_state(), [5, 5]);
    assert_eq!(maze.get_allowed_actions(), ['U']);
    assert_eq!(maze.is_done(), true);
}