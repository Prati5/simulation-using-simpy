import simpy
import random


class ContainerTerminal:
    """
    Represents a container terminal with loading and unloading operations.
    """

    def __init__(self, env, num_cranes, num_gates, num_trucks):
        self.env = env
        self.cranes = simpy.Resource(env, num_cranes)
        self.gates = simpy.Resource(env, num_gates)
        self.trucks = simpy.Resource(env, num_trucks)
        self.containers_loaded = 0
        self.containers_unloaded = 0

    def load_container(self, container):
        """Load a container onto a crane for loading onto a ship."""
        yield self.env.timeout(random.uniform(1, 3))
        self.containers_loaded += 1
        print(f"Container {container} loaded at {self.env.now}")

    def unload_container(self, container):
        """Unload a container from the terminal."""
        yield self.env.timeout(random.uniform(1, 3))
        self.containers_unloaded += 1
        print(f"Container {container} unloaded at {self.env.now}")


def truck(env, name, terminal):
    """
    Simulates a truck arriving at and leaving the container terminal.
    """
    print(f"{name} arriving at gate at {env.now}")
    with terminal.gates.request() as request:
        yield request
        print(f"{name} entering terminal at {env.now}")
        with terminal.trucks.request() as truck_request:
            yield truck_request
            yield env.process(terminal.unload_container(name))
        print(f"{name} leaving terminal at {env.now}")


def generate_trucks(env, terminal):
    """
    Generates trucks at the container terminal.

    Parameters:
    - env: The simulation environment.
    - terminal: The container terminal object.
    """
    truck_id = 0
    while True:
        env.process(truck(env, f"Truck-{truck_id}", terminal))
        yield env.timeout(random.expovariate(1 / 5))
        truck_id += 1


def vessel(env, name, terminal):
    """
    Simulates a vessel arriving at and leaving the container terminal.

    Parameters:
    - env: The simulation environment.
    - name: The name of the vessel.
    - terminal: The container terminal object.
    """
    print(f"{name} arriving at terminal at {env.now}")
    with terminal.gates.request() as request:
        yield request
        print(f"{name} berthing at {env.now}")
        with terminal.cranes.request() as crane_request:
            yield crane_request
            print(f"{name} starting unloading at {env.now}")
            yield env.process(terminal.unload_container(name))
        print(f"{name} departing from terminal at {env.now}")


def generate_vessels(env, terminal):
    """
    Generates vessels at the container terminal.
    Parameters:
    - env: The simulation environment.
    - terminal: The container terminal object.
    """
    vessel_id = 0
    while True:
        env.process(vessel(env, f"Vessel-{vessel_id}", terminal))
        yield env.timeout(random.expovariate(1 / 5))
        vessel_id += 1


def run_simulation(env, simulation_time):
    """
    Runs the simulation for a specified duration.

    Parameters:
    - env: The simulation environment.
    - simulation_time: The duration of the simulation.
    """
    terminal = ContainerTerminal(env, num_cranes=2, num_gates=1, num_trucks=3)
    env.process(generate_trucks(env, terminal))
    env.process(generate_vessels(env, terminal))
    yield env.timeout(simulation_time)


def main():
    """
    Main function to initialize and run the simulation.
    """
    env = simpy.Environment()
    simulation_time = 50
    env.process(run_simulation(env, simulation_time))
    env.run(until=simulation_time)
    print("Simulation finished.")


if __name__ == "__main__":
    main()
