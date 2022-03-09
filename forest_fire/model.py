from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from .agent import TreeCell
from mesa.batchrunner import *
import datetime


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, burn_dens=0.05, ext_prob=0.5):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)
        self.ext_prob = ext_prob

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.

                
                if x == 0:
                    new_tree.condition = "On Fire"

                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        #Cria pequenos clusters de árvores já queimadas
        for (contents, x, y) in self.grid.coord_iter(): 
            pos = (x, y)
            for neighbor in self.grid.neighbor_iter(pos):
                if neighbor.condition == "Fine" and self.random.random() < burn_dens:   
                    neighbor.condition = "Burned Out"

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

def saved_trees(model):
    fine_trees = sum(1 for agent in model.schedule.agents if agent.condition == "Fine")
    trees = sum(1 for agent in model.schedule.agents)
    return fine_trees/trees
    

#0.01, 0.02, 0.03
def batch_run():
    b_dens = 0.03
    fixed_params= {
        "height": 100,
        "width": 100,
        "burn_dens": b_dens,
        "ext_prob": 0.5,
        
        
    }
    variable_params = {
        "density": [0.2,0.4,0.6,0.8],
    }

    experiments_per_parameter_configuration = 10
    max_steps_per_simulation = 10

    batch_run = BatchRunner(ForestFire, 
        variable_params, 
        fixed_params,
        iterations = experiments_per_parameter_configuration,
        max_steps = max_steps_per_simulation,
        model_reporters = {
            "Saved_trees": saved_trees
        },
        agent_reporters = {
            "Condition": "condition",
        }
        )

    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    run_agent_data = batch_run.get_agent_vars_dataframe()

    now = str(datetime.datetime.now()).replace(" ","_").replace(".","_").replace(":","_")
    file_name_suffix = ("_burn_dens_"+"30"+"ext_prob_"+"50"+"_iter_"+str(experiments_per_parameter_configuration)+"_steps_"+str(max_steps_per_simulation)+"_"+now)
    run_model_data.to_csv("model_data"+file_name_suffix+".csv")
    run_agent_data.to_csv("agent_data"+file_name_suffix+".csv")
