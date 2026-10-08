"""
Simulating truss designs
DOCS: https://anastruct.readthedocs.io/en/latest/getting_started.html

NOTE: Displacement is highly exaggerated as the bridge is built out of normal elements
    instead of truss elements.
"""

from anastruct import SystemElements
from typing import Dict
from bridgeModels import BridgeModels as BM

class Bridge():
    def __init__(self):
        """
        sets up a bridge with the material properties of uncooked spaghetti
        """
        self.weight = 0.11 #weight per meter
        self.E = 5e9  #Young's modulus (Pa) 2.4-5GPa
        self.yield_strength = 3e5  #Yield strength (Pa)
        self.diameter = 0.01 #diameter of members
        self.A = 3.1416 * (self.diameter / 2) ** 2 #cross sectional area
        self.I = (3.1416 / 64) * self.diameter ** 4 #moment of inertia
        self.c = self.diameter / 2 #distance to outer fiber
        self.max_deflection = 0.006  # 6 mm

        self.ss = SystemElements(EA=self.E*self.A, EI=self.E*self.I) #init model
    
    def build(self, model: list):
        """
        builds bridge with elements and 2 fixed supports
        """

        #builds base of the bridge
        base = model["base"]
        self.ss.add_multiple_elements(
            location=(base[0], base[1]), 
            n=model["subdivision"], 
            g=self.weight, 
            mp={1: 0.02, 2: 0.02}
        )

        #builds the rest of the bridge
        truss = bm.generateTruss(model=model, baseElements=self.getElements())
        for e in truss:
            self.ss.add_element(location=[e[0], e[1]], g=self.weight, mp={1: 0.02, 2: 0.02})

        #adds support to the bridge
        self.ss.add_support_fixed(node_id=1)
        self.ss.add_support_fixed(node_id=model["subdivision"]+1)

    def applyLoad(self, mass: float, node=-1, element=-1):
        """
        Applies a mass in kg to a given node or element
        """
        
        Fy = mass*9.81 #9.81 gravity
        if node > 0:
            self.ss.point_load(node_id=node, Fy=-Fy)
        elif element > 0:
            self.ss.q_load(element_id=element, q=-Fy)
        else:
            raise ValueError("Node or element id was not given or invalid node or element id was given")

    def showStruct(self, mode=""):
        """
        shows the structure and the results of the simulation

        given a specific mode it will show the specific graph
        """
        
        self.ss.show_structure()
        if mode == "":
            self.ss.show_results()
        elif mode == "displacement":
            self.ss.show_displacement()
        elif mode == "axial_force":
            self.ss.show_axial_force()
        elif mode == "bending_moment":
            self.ss.show_bending_moment()
        elif mode == "reaction_force":
            self.ss.show_reaction_force()
        elif mode == "shear_force":
            self.ss.show_shear_force()

    def solve(self):
        """
        solves the structure
        """

        self.ss.solve(verbosity=0, max_iter=1000, geometrical_non_linear=False)

    def getElements(self) -> Dict[int, object]:
        """
        returns the element_map of the structure
        """
        
        return self.ss.element_map

    def checkFailure(self, element_id: int):
        """
        Checks if an element failed due to bending stress, axial stress, or excessive deflection.
        Prints the failure reason if any threshold is exceeded.
        """

        # Get element results
        result = self.ss.get_element_results(element_id)
        if not result:
            print(f"Element {element_id} has no result data.")
            return

        # Extract max internal forces
        moment = result.get("Mmax", 0)
        axial_force = result.get("Nmax", 0)

        # Calculate stresses
        bending_stress = (moment * self.c) / self.I if self.I else 0
        axial_stress = axial_force / self.A if self.A else 0

        # Check stress failures
        if bending_stress > self.yield_strength:
            print(f"Element {element_id} failed due to bending stress: {bending_stress:.2e} Pa")
        if axial_stress > self.yield_strength:
            print(f"Element {element_id} failed due to axial stress: {axial_stress:.2e} Pa")

        # Check nodal deflection
        nodes = result.get("nodes", [])
        displacements = self.ss.get_node_displacements()
        for node_id in nodes:
            if node_id in displacements:
                dy = abs(displacements[node_id][1])  # vertical displacement
                if dy > self.max_deflection:
                    print(f"Element {element_id} failed due to node {node_id} exceeding deflection: {dy:.4f} m")


if __name__ == "__main__":
    #retrieving model from bridgeModels
    bm = BM(
        start=[0,0],
        end=[0.6,0],
        subdivisions=10
    )

    model = bm.getModel(6)
    mass = 1

    #building bridge
    bridge = Bridge()
    #built left to right, base first and then the triangles
    bridge.build(model)

    #applying a load to the bridge
    bridge.applyLoad(element=4, mass=mass)
    # bridge.applyLoad(node=7, mass=mass)

    try:
        #results
        bridge.solve()

        #checking for points of failure in the structure
        for i in list(bridge.getElements().keys()):
            bridge.checkFailure(i)
    except Exception as e:
        print(f"Model was not able to be solved:\n{e}")


    input(f"Current Load: {9.81*mass}\nPress enter to see graphs.")
    bridge.showStruct() #displacement to see only displacement