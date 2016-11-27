import numpy as np


class Simulator:
    def __init__(self, main, f1, f2):
        self.pos = (0, 19)
        self.dir = 1  # 0=North, 1=East, 2=South, 3=West
        self.n_commands = 0
        self.debug = False
        self.f1 = f1
        self.f2 = f2
        self.main = main
        self._map = np.load('./qvik_array.npy')[:, :, 0]

    def _print_position(self):
        if self.debug:
            print('({p1}, {p2})'.format(p1=self.pos[0], p2=self.pos[1]))

    def _move(self, l):
        """Move

        :param l: Step length: 1 for forward, -1 for backward
        """

        if self.dir == 0:
            next_pos = (self.pos[0], self.pos[1] - l)  # Up
        elif self.dir == 1:
            next_pos = (self.pos[0] + l, self.pos[1])  # Right
        elif self.dir == 2:
            next_pos = (self.pos[0], self.pos[1] + l)  # Down
        else:
            next_pos = (self.pos[0] - l, self.pos[1])  # Left

        # Next step is inside the map and is not a wall -> move to next step
        if 0 <= self.pos[0] < 20 and 0 <= self.pos[1] < 20 and self._map[next_pos[1]][next_pos[0]]:
            self.pos = next_pos
        self._print_position()
        self.n_commands += 1

        if self.pos == (19, 0):
            # Goal reached
            print('Success with configuration')
            print(self.n_commands)
            print(self.main)
            print(self.f1)
            print(self.f2)
            raise ValueError(1)

    def forward(self):
        self._move(1)

    def backward(self):
        self._move(-1)

    def right(self):
        self.dir += 1
        if self.dir == 4:
            self.dir = 0

    def left(self):
        self.dir -= 1
        if self.dir == -1:
            self.dir = 3

    def _run_command(self, command_name):
        if self.n_commands > 1000:
            if self.debug:
                print('Max steps exceeded')
            raise ValueError(-1)

        if command_name == 'forward':
            self.forward()
        elif command_name == 'backward':
            self.backward()
        elif command_name == 'right':
            self.right()
        elif command_name == 'left':
            self.left()
        elif command_name == 'f1':
            for com in self.f1:
                self._run_command(com)
        elif command_name == 'f2':
            for com in self.f2:
                self._run_command(com)

    def run(self):
        self._print_position()
        for com in self.main:
            self._run_command(com)
        if self.debug:
            print('Did not reach goal')
        raise ValueError(0)

if __name__ == '__main__':
    s = Simulator(
        ['f1'],
        ['forward', 'f2'],
        ['left', 'forward']
    )
    s.debug = True
    s.run()
