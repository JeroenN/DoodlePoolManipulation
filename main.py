from environment import Environment
import strategies
import quick_sort

# Right now this function creates agents with the standard strategy
# storing these agents might not be necessary anymore because it is stored in the environment now 
def create_agents(n_agents, n_pop_agents, environment):
    agents = []
    for i in range(n_agents):
        agent = strategies.Standard(environment, i)
        agents.append(agent)
    for i in range(n_pop_agents):
        agents.append(strategies.Popular(environment, i+n_agents))

    return agents

def create_environment(n_time_slots):
    return Environment(n_time_slots)

def print_game(environment, agents):
    print(environment, '\n')
    #print('\n'.join(map(str, agents)))
    # agents[0].print_voted_time_slots()
    # agents[0].print_time_slot_preference()

def let_agents_vote(agents, environment):
    idx = environment.get_index_agent_willingness()
    while idx is not None:
        agent = agents[idx]
        agent.vote()  # Agents vote for their preferred time slots
        idx = environment.get_index_agent_willingness()

def let_agents_calculate_utility(agents):
    for agent in agents:
        agent.calculate_utility()
        agent.change_time_slot_preference()

def calculate_social_welfare(environment, agents, rounds):
    social_welfare = 0
    for agent in agents:
        social_welfare += agent.get_utility()
    
    return social_welfare

def calculate_egalitarian_welfare(agents, rounds):
    welfares = []
    welfare_idx = []

    for idx, agent in enumerate(agents):
        welfares.append(agent.get_utility())
        welfare_idx.append(idx)

    quick_sort.quick_sort(welfares, welfare_idx, 0, len(agents)-1)

    return welfares[0], welfares[len(agents)-1]

def print_game_results(environment, agents, rounds, social_welfare, min_utility, max_utility):
    print("Game ended! \n")
    for agent in agents:
        print(agent, f", Strategy: {agent.get_strategy()}, Average utility: {agent.get_utility()/rounds}")

    print(f'\nSocial welfare: ', social_welfare/rounds)
    print(f'\nMean utility; ', (social_welfare/len(agents))/rounds)

    print(f"\nMinimum utility ", min_utility/rounds) # agent with smallest utility
    print(f"\nMaximum utility: ", max_utility/rounds) # agent with largest utility

def play_game(environment, agents):
    rounds = 10000
    social_welfare=0
    min_utility=0
    max_utility=0
    print("Playing game...")

    for _ in range(rounds):
        let_agents_vote(agents, environment)
        environment.determine_most_popular_time_slot()
        let_agents_calculate_utility(agents)
        social_welfare += calculate_social_welfare(environment, agents, rounds)
        min, max = calculate_egalitarian_welfare(agents, rounds)
        min_utility += min
        max_utility += max
        environment.reset_enviroment(agents)

    environment.rank_popularity_time_slots()
    print_game_results(environment, agents, rounds, social_welfare, min_utility, max_utility)

def main():
    environment = create_environment(
        int(input("How many dates are in the Doodle poll?: ")))  # create and store environment
    agents = create_agents(int(input("How many standard voters are in the Doodle poll?: ")), int(input("How many popular voters are in the Doodle poll?: ")),
                           environment)  # create and store agents
    environment.determine_willingness(agents)
    environment.rank_willingness()
    play_game(environment, agents)



if __name__ == "__main__":
    main()
