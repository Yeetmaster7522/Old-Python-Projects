"""
Simulating truss designs
DOCS: https://anastruct.readthedocs.io/en/latest/getting_started.html
"""

from anastruct import SystemElements
from typing import Dict
from bridgeModels import BridgeModels as BM
import math

class Bridge():
    def __init__(self):
        """
        sets up a bridge with the material properties of uncooked spaghetti
        """
        self.weight = 0.0099 / 1000 #weight per meter (kN/m)
        self.E = 3e9  #Young's modulus (Pa)
        self.UTS = 3.0e6*0.9  #UTS (Pa)
        self.diameter = 0.01 #diameter of members
        self.A = math.pi * (self.diameter / 2) ** 2 #cross sectional area
        self.I = (math.pi / 64) * self.diameter ** 4 #moment of inertia
        self.c = self.diameter / 2 #distance to outer fiber
        self.max_deflection = 0.006  # breaking point

        EA = (self.E*self.A) / 1000
        self.ss = SystemElements(EA=EA) #init model
    
    def build(self, model: list):
        """
        builds bridge with elements and 2 fixed supports
        """

        #builds base of the bridge
        base = model["base"]
        x0, y0 = base[0]
        x1, y1 = base[1]
        dx = (x1 - x0) / model["subdivision"]
        dy = (y1 - y0) / model["subdivision"]
        for i in range(model["subdivision"]):
            start = [x0 + i*dx, y0 + i*dy]
            end = [x0 + (i+1)*dx, y0 + (i+1)*dy]
            self.ss.add_truss_element(location=[start, end])

        #builds the rest of the bridge
        truss = bm.generateTruss(model=model, baseElements=self.getElements())
        for e in truss:
            self.ss.add_truss_element(location=[e[0], e[1]])

        #adds support to the bridge
        self.ss.add_support_hinged(node_id=1)
        self.ss.add_support_roll(node_id=model["subdivision"]+1)

        # for eid in self.ss.element_map.keys():
        #     self.ss.q_load(element_id=eid, q=-self.weight)

    def applyLoad(self, mass: float, node=-1, element=-1):
        """
        Applies a mass in kg to a given node or element
        """
        
        Fy = (mass * 9.81) / 1000
        if node > 0 and mass > 0:
            self.ss.point_load(node_id=node, Fy=-Fy)
        elif element > 0 and mass > 0:
            self.ss.q_load(element_id=element, q=-Fy)
        else:
            raise ValueError("""
                Node or element id was not given or invalid node or element id was given
                or
                No mass was applied
                """)

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

        self.ss.solve(verbosity=0, max_iter=1000, geometrical_non_linear=True)

    def getElements(self) -> Dict[int, object]:
        """
        returns the element_map of the structure
        """
        
        return self.ss.element_map

    def checkFailure(self):
        """
        Checks if elements failed and prints what happened
        """

        members = self.ss.get_element_results()

        for m in members:
            # print(m)
            #tension fracture check (axial stress)
            tension = max(abs(m["Nmax"]), abs(m["Nmin"])) * 1000 / self.A
            if tension > self.UTS:
                print(f"    {m["id"]}: tension fracture")

            #euler buckling check (compression members)
            K = 1.7
            Pcr = (math.pi**2 * self.E * self.I) / (K * m["length"])**2
            Ncomp = None
            if m["Nmax"] < 0:
                Ncomp = m["Nmax"] * 1000
            if m["Nmin"] < 0 and (Ncomp is None or m["Nmin"]*1000 < Ncomp):
                Ncomp = m["Nmin"] * 1000
            if Ncomp is not None and abs(Ncomp) > Pcr:
                print(f"    {m["id"]}: compression buckling")

            #deflection check
            deflection = max(abs(m["wtotmax"]), abs(m["wtotmin"]))
            if deflection > self.max_deflection:
                print(f"    {m["id"]}: excessive sagging")


if __name__ == "__main__":
    #retrieving model from bridgeModels
    bm = BM(
        start=[0,0],
        end=[0.6,0],
        subdivisions=10
    )

    model = bm.getModel(2)
    mass = 3

    #building bridge
    bridge = Bridge()
    #built left to right, base first and then the triangles
    bridge.build(model)

    #applying a load to the bridge
    bridge.applyLoad(node=1, mass=mass)
    # bridge.applyLoad(node=2, mass=mass)

    try:
        #results
        bridge.solve()

        #checking for points of failure in the structure
        # bridge.checkFailure()
    except Exception as e:
        print(f"Model was not able to be solved:\n{e}")

        # Geometry context
        print("Total nodes:", len(bridge.ss.node_map))
        print("Node IDs:", list(bridge.ss.node_map.keys()))
        print("Total elements:", len(bridge.ss.element_map))
        print("Element IDs:", list(bridge.ss.element_map.keys()))

        # Node results (list of dicts) — safe even if solve failed partway
        try:
            res_nodes = bridge.ss.get_node_results_system()
            print("Node results count:", len(res_nodes))
            for r in res_nodes:
                nid = r.get("id", r.get("node_id", "?"))
                print(f"Node {nid}: {r}")
        except Exception as rn_err:
            print("Node results not available:", rn_err)

        # Show which nodes you intended to load/support (from your own inputs)
        print("Intended point loads on nodes:", [3, 4])
        print("Intended supports: hinged at node 1, roller at node", model["subdivision"] + 1)

    input(f"Current load: mass={mass}, weight={mass*9.81}\nPress enter to show graphs")
    bridge.showStruct()