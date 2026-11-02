#Olmard Guillaume


# Problem 3 Human - Predator - Prey Simulation




"""Simulate prey, predators, and humans living on an island."""

import random
import matplotlib.pyplot as plt


class Island:
    """Represent an island grid containing prey, predators, and humans."""

    def __init__(
        self,
        size: int,
        initial_prey: int,
        initial_predators: int,
        count_humans: int,
    ) -> None:
        """Initialize the island and randomly place its starting animals.

        Preconditions:
            Size must be positive. Animal counts must be nonnegative.
            The total number of animals cannot exceed the grid capacity.
        Postconditions:
            The grid contains the requested starting populations.
        """
        if size <= 0:
            raise ValueError("Island size must be greater than zero.")

        if min(initial_prey, initial_predators, count_humans) < 0:
            raise ValueError("Animal counts cannot be negative.")

        if initial_prey + initial_predators + count_humans > size * size:
            raise ValueError("Too many animals for the island size.")

        self.size: int = size
        self.grid: list[list[Animal | int]] = [
            [0 for _ in range(size)] for _ in range(size)
        ]

        self.init_animals(initial_prey, initial_predators, count_humans)

    def init_animals(
        self,
        count_prey: int,
        count_predators: int,
        count_humans: int,
    ) -> None:
        """Randomly place the starting populations on empty grid cells."""
        for _ in range(count_prey):
            self.add_random_animal(Prey)

        for _ in range(count_predators):
            self.add_random_animal(Predator)

        for _ in range(count_humans):
            self.add_random_animal(Human)

    def add_random_animal(
        self, animal_type: type["Animal"]
    ) -> "Animal | None":
        """Create an animal at a random empty cell, if one is available."""
        empty_cells: list[tuple[int, int]] = [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if self.grid[x][y] == 0
        ]

        if not empty_cells:
            return None

        x, y = random.choice(empty_cells)
        return animal_type(self, x, y)

    def register(self, animal: "Animal") -> None:
        """Place an animal in its current grid cell."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: "Animal") -> None:
        """Remove an animal if it still occupies its recorded grid cell."""
        if self.grid[animal.x][animal.y] is animal:
            self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> "Animal | int":
        """Return a cell's contents, or -1 if its coordinates are out of bounds."""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[x][y]

        return -1

    def count_prey(self) -> int:
        """Return the current number of prey on the island."""
        return sum(
            isinstance(animal, Prey)
            for row in self.grid
            for animal in row
        )

    def count_predators(self) -> int:
        """Return the current number of predators on the island."""
        return sum(
            isinstance(animal, Predator)
            for row in self.grid
            for animal in row
        )

    def count_humans(self) -> int:
        """Return the current number of humans on the island."""
        return sum(
            isinstance(animal, Human)
            for row in self.grid
            for animal in row
        )

    def __str__(self) -> str:
        """Return the island grid as a printable string."""
        return "\n".join(
            " ".join(
                str(animal) if animal != 0 else "."
                for animal in row
            )
            for row in self.grid
        )


class Animal:
    """Base class for organisms living on the island."""

    def __init__(
        self,
        island: Island,
        x: int,
        y: int,
        symbol: str,
    ) -> None:
        """Initialize an animal and register it on the island."""
        self.island: Island = island
        self.x: int = x
        self.y: int = y
        self.symbol: str = symbol
        self.moved: bool = False

        self.island.register(self)

    def __str__(self) -> str:
        """Return the character used to represent this animal."""
        return self.symbol

    def check_grid(
        self, type_looking_for: type = int
    ) -> tuple[int, int] | int:
        """Find a random neighboring cell containing the requested type.

        Parameters:
            type_looking_for: An Animal subclass, or int to search for
                an empty cell.
        Returns:
            Coordinates of a matching neighboring cell, or 0 if none exists.
        """
        neighbors: list[tuple[int, int]] = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1),
        ]

        random.shuffle(neighbors)

        for dx, dy in neighbors:
            new_x: int = self.x + dx
            new_y: int = self.y + dy
            neighbor = self.island.animal(new_x, new_y)

            # Only an actual empty cell (0) is a valid movement destination.
            # The value -1 means the coordinates are outside the island.
            if type_looking_for is int:
                if neighbor == 0:
                    return new_x, new_y
            elif isinstance(neighbor, type_looking_for):
                return new_x, new_y

        return 0

    def move(self) -> None:
        """Move to a random neighboring empty cell if one is available."""
        if self.moved:
            return

        location = self.check_grid(int)

        if location != 0:
            new_x, new_y = location

            self.island.remove(self)
            self.x = new_x
            self.y = new_y
            self.island.register(self)

        self.moved = True

    def breed(self) -> None:
        """Create an offspring in a neighboring empty cell if possible."""
        location = self.check_grid(int)

        if location != 0:
            new_x, new_y = location
            type(self)(self.island, new_x, new_y)

    def reset_moved(self) -> None:
        """Allow the animal to move during the next simulation tick."""
        self.moved = False


class Prey(Animal):
    """Represent prey that move and reproduce."""

    breed_time: int = 3

    def __init__(self, island: Island, x: int, y: int) -> None:
        """Create prey with its breeding clock initialized."""
        super().__init__(island, x, y, "p")
        self.breed_clock: int = Prey.breed_time

    def clock_tick(self) -> None:
        """Decrease the breeding clock and reproduce when it expires."""
        self.breed_clock -= 1

        if self.breed_clock <= 0:
            self.breed()
            self.breed_clock = Prey.breed_time


class Predator(Animal):
    """Represent predators that hunt prey and can starve."""

    breed_time: int = 6
    starve_time: int = 3

    def __init__(self, island: Island, x: int, y: int) -> None:
        """Create a predator with breeding and starvation clocks."""
        super().__init__(island, x, y, "X")
        self.starve_clock: int = Predator.starve_time
        self.breed_clock: int = Predator.breed_time

    def eat(self) -> bool:
        """Eat a neighboring prey and move into its cell.

        Return True if prey was eaten; otherwise return False.
        """
        location = self.check_grid(Prey)

        if location == 0:
            return False

        prey_x, prey_y = location
        prey = self.island.animal(prey_x, prey_y)

        if not isinstance(prey, Prey):
            return False

        self.island.remove(prey)
        self.island.remove(self)

        self.x = prey_x
        self.y = prey_y

        self.island.register(self)
        self.starve_clock = Predator.starve_time

        return True

    def clock_tick(self) -> None:
        """Update the clocks, starve if necessary, and reproduce when due."""
        self.starve_clock -= 1
        self.breed_clock -= 1

        if self.starve_clock <= 0:
            self.island.remove(self)
            return

        if self.breed_clock <= 0:
            self.breed()
            self.breed_clock = Predator.breed_time


class Human(Animal):
    """Represent humans that hunt predators, reproduce, and can starve."""

    breed_time: int = 9
    starve_time: int = 5
    hunt_time: int = 2

    def __init__(self, island: Island, x: int, y: int) -> None:
        """Create a human with separate hunt, breeding, and starvation clocks."""
        super().__init__(island, x, y, "H")

        self.hunt_clock: int = Human.hunt_time
        self.starve_clock: int = Human.starve_time
        self.breed_clock: int = Human.breed_time

    def eat(self) -> bool:
        """Kill a neighboring predator and move into its cell.

        Return True if a predator was killed; otherwise return False.
        """
        location = self.check_grid(Predator)

        if location == 0:
            return False

        predator_x, predator_y = location
        predator = self.island.animal(predator_x, predator_y)

        if not isinstance(predator, Predator):
            return False

        self.island.remove(predator)
        self.island.remove(self)

        self.x = predator_x
        self.y = predator_y

        self.island.register(self)
        self.starve_clock = Human.starve_time

        return True

    def take_turn(self) -> None:
        """Hunt on schedule, move when not hunting successfully, and update clocks."""
        self.hunt_clock -= 1
        hunted_successfully: bool = False

        self.starve_clock -= 1

        if self.hunt_clock <= 0:
            hunted_successfully = self.eat()
            self.hunt_clock = Human.hunt_time

        if not hunted_successfully:
            self.move()

        if self.starve_clock <= 0:
            self.island.remove(self)
            return

        self.breed_clock -= 1

        if self.breed_clock <= 0:
            self.breed()
            self.breed_clock = Human.breed_time


def main(
    predator_breed_time: int = 6,
    predator_starve_time: int = 3,
    initial_predators: int = 10,
    prey_breed_time: int = 3,
    initial_prey: int = 50,
    size: int = 10,
    initial_humans: int = 2,
    human_breed_time: int = 9,
    human_starve_time: int = 5,
    human_hunt_time: int = 2,
    ticks: int = 1000,
) -> None:
    """Run the island simulation and graph the three population histories.

    Stop when the population counts remain unchanged for ten consecutive
    ticks, or when the maximum of 1000 ticks is reached.
    """
    if min(
        predator_breed_time,
        predator_starve_time,
        prey_breed_time,
        human_breed_time,
        human_starve_time,
        human_hunt_time,
    ) <= 0:
        raise ValueError("Breeding, starvation, and hunt times must be positive.")

    if ticks < 0:
        raise ValueError("Ticks cannot be negative.")

    Prey.breed_time = prey_breed_time

    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time

    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    island = Island(
        size,
        initial_prey,
        initial_predators,
        initial_humans,
    )

    print("Island at the beginning:")
    print(island)

    prey_history: list[int] = []
    predator_history: list[int] = []
    human_history: list[int] = []

    previous_counts: tuple[int, int, int] | None = None
    stable_ticks: int = 0
    maximum_ticks: int = min(ticks, 1000)

    for tick in range(maximum_ticks):
        # Snapshot the population so newborn animals wait until the next tick.
        animals: list[Animal] = [
            animal
            for row in island.grid
            for animal in row
            if isinstance(animal, Animal)
        ]

        random.shuffle(animals)

        for animal in animals:
            animal.reset_moved()

        for animal in animals:
            # Skip an animal if it was eaten or removed earlier this tick.
            if island.animal(animal.x, animal.y) is not animal:
                continue

            if isinstance(animal, Human):
                animal.take_turn()

            elif isinstance(animal, Predator):
                ate_prey: bool = animal.eat()

                if island.animal(animal.x, animal.y) is not animal:
                    continue

                if not ate_prey:
                    animal.move()

                animal.clock_tick()

            elif isinstance(animal, Prey):
                animal.move()

                if island.animal(animal.x, animal.y) is not animal:
                    continue

                animal.clock_tick()

        prey_count: int = island.count_prey()
        predator_count: int = island.count_predators()
        human_count: int = island.count_humans()

        prey_history.append(prey_count)
        predator_history.append(predator_count)
        human_history.append(human_count)

        if tick % 10 == 0:
            print(
                f"Tick {tick}: Prey = {prey_count}, "
                f"Predators = {predator_count}, Humans = {human_count}"
            )

        current_counts: tuple[int, int, int] = (
            prey_count,
            predator_count,
            human_count,
        )

        if current_counts == previous_counts:
            stable_ticks += 1
        else:
            stable_ticks = 0

        previous_counts = current_counts

        if stable_ticks >= 10:
            print(f"All three populations stabilized at tick {tick}.")
            break

    print("\nIsland at the end:")
    print(island)

    time_points: range = range(1, len(prey_history) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(time_points, prey_history, label="Prey")
    plt.plot(time_points, predator_history, label="Predators")
    plt.plot(time_points, human_history, label="Humans")

    plt.xlabel("Time (ticks)")
    plt.ylabel("Population")
    plt.title("Prey, Predator, and Human Populations Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save a chart image for insertion into the assignment document.
    plt.savefig("p3_population_chart.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
