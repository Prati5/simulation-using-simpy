import simpy
import random


class ContainerTerminal:
    def __init__(self, env, num_cranes, num_gates):
        self.env = env
        self.cranes = simpy.Resource(env, num_cranes)
        self.gates = simpy.Resource(env, num_gates)
        self.containers_loaded = 0
        self.containers_unloaded = 0

    def load_container(self, container):
        """
        Load a container onto a crane for loading onto a ship.
        Parameters: - container: The container to be loaded onto the crane.
        """
        yield self.env.timeout(random.uniform(1, 3))  
        self.containers_loaded += 1
        print(f"Container {container} loaded at {self.env.now}")

    def unload_container(self, container):
        """
            Unload a container from the terminal.
            Parameters:- container: The container to be unloaded.
        """
        yield self.env.timeout(random.uniform(1, 3))  
        self.containers_unloaded += 1
        print(f"Container {container} unloaded at {self.env.now}")


def truck(env, name, terminal):
    """
        This function represents a truck arriving at a container terminal.
        Parameters:
        - env: The simulation environment.
        - name: The name of the truck.
        - terminal: The container terminal object.

        Yields:
        - The arrival time of the truck at the gate.
        - The entrance time of the truck into the terminal.
        - The unloading process of the truck.
        - The departure time of the truck from the terminal.

    """
    print(f"{name} arriving at gate at {env.now}")
    with terminal.gates.request() as request:
        yield request
        print(f"{name} entering terminal at {env.now}")
        yield env.process(terminal.unload_container(name))
        print(f"{name} leaving terminal at {env.now}")


def generate_trucks(env, terminal):
    """
        Generate trucks at a container terminal.
        This method generates trucks at a container terminal in a simulation environment. 
    """
    truck_id = 0
    while True:
        env.process(truck(env, f"Truck-{truck_id}", terminal))
        yield env.timeout(random.expovariate(1 / 5))  
        truck_id += 1


def run_simulation(env):
    terminal = ContainerTerminal(env, num_cranes=2, num_gates=1)
    env.process(generate_trucks(env, terminal))
    yield env.timeout(50)  # Run simulation for 50 time units


# Main function to initialize and run the simulation
def main():
    env = simpy.Environment()
    env.process(run_simulation(env))
    env.run(until=50)

    print("Simulation finished.")


if __name__ == "__main__":
    main()
