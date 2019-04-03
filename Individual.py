class Individual:

    ncity = 0

    def __init__(self,node_list = [], split_list = [], ptl = [], C1 = [], C2 = []):
        self.NL = node_list
        self.SL = split_list
        self.PTL = ptl
        self.C1 = C1
        self.C2 = C2

    def __str__(self):
        s = "Node List           : "+ " ".join(str(e) for e in self.NL) + "\n" + \
            "Processing Time List: "+ " ".join(str(e) for e in self.PTL) + "\n"+ \
            "Split List : "+ " ".join(str(e) for e in self.SL) + "\n" +\
            "C1 : " + " ".join(str(e) for e in self.C1) + "\n" +\
            "C2 : " + " ".join(str(e) for e in self.C2) + "\n"
        return s

    def compute_SL(self):
        sl = [0 for _ in range(Individual.ncity)]
        for node in self.NL:
            sl[node] += 1
        return sl


