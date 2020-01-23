class Model:
    """ A Model holds the parameters of a disease.

    Main attributes:
    - LVS_damage    - P(LVS=1|Seq)
    - LGS_damage    - P(LGS=1|Seq)
    - HGS_damage    - P(HGS=1|Seq)
    - HVS_damage    - P(HVS=1|Seq)
    - ENV_penetrance    - P(D=1|HVS=1,Cov)
    - LVS_penetrance    - P(D=1|HVS=0,HGS=1,Cov)
    - LGS_penetrance    - P(D=1|HVS=0,HGS=0,LGS=1,Cov)
    - HGS_penetrance    - P(D=1|HVS=0,HGS=0,LGS=0,LVS=1,Cov)
    - HVS_penetrance    - P(D=1,HVS=0,HGS=0,LGS=0,LVS=0,Cov)


    >>> d1 = Model(0.5, 0.5, 0.5, 0.5, 0.6, 0, 0, 0, 0)
    >>> d1.runModel()
    0.0375
    
    """

    def __init__(self):
        self.LVS_damage = 'NA'
        self.LGS_damage = 'NA'
        self.HGS_damage = 'NA'
        self.HVS_damage = 'NA'
        self.ENV_penetrance = 'NA'
        self.LVS_penetrance = 'NA'
        self.LGS_penetrance = 'NA'
        self.HGS_penetrance = 'NA'
        self.HVS_penetrance = 'NA'

    def setValues(self, 
                 LVS_damage, LGS_damage, HGS_damage, HVS_damage,
                 ENV_penetrance, LVS_penetrance, LGS_penetrance, 
                 HGS_penetrance, HVS_penetrance):
        self.LVS_damage = float(LVS_damage)
        self.LGS_damage = float(LGS_damage)
        self.HGS_damage = float(HGS_damage)
        self.HVS_damage = float(HVS_damage)
        self.ENV_penetrance = float(ENV_penetrance)
        self.LVS_penetrance = float(LVS_penetrance)
        self.LGS_penetrance = float(LGS_penetrance)
        self.HGS_penetrance = float(HGS_penetrance)
        self.HVS_penetrance = float(HVS_penetrance)

    def runModel(self):
        """ Compute P(D=1|Cov,Seq) 
           = sum(P(D=1|HVS,HGS,LGS,LVS,Cov)*P(HVS|Seq)*P(HGS|Seq)*P(LGS|Seq)*P(LVS|Seq))
           (See model-parameter.ppt slide 7)
        """

        if self.LVS_damage == 'NA' or self.LGS_damage == 'NA' or\
            self.HGS_damage == 'NA' or self.HVS_damage == 'NA' or\
            self.ENV_penetrance == 'NA' or self.LVS_penetrance == 'NA' or\
            self.LGS_penetrance == 'NA' or self.HGS_penetrance == 'NA' or\
            self.HVS_penetrance == 'NA':
            return 'NA'

        return ( self.HVS_penetrance * self.HVS_damage + 
                 self.HGS_penetrance * (1 - self.HVS_damage) * self.HGS_damage + 
                 self.LGS_penetrance * (1 - self.HVS_damage) * (1 - self.HGS_damage) 
                                     * self.LGS_damage +
                 self.LVS_penetrance * (1 - self.HVS_damage) * (1 - self.HGS_damage) 
                                     * (1 - self.LGS_damage) * self.LVS_damage + 
                 self.ENV_penetrance * (1 - self.HVS_damage) * (1 - self.HGS_damage) 
                                     * (1 - self.LGS_damage) * (1 - self.LVS_damage) )

#        return ( (self.HVS_penetrance * self.HVS_damage +
#                 self.HGS_penetrance * (1 - self.HVS_damage) * self.HGS_damage +
#                 self.LGS_penetrance * (1 - self.HVS_damage) * (1 - self.HGS_damage)
#                                     * self.LGS_damage +
#                 self.LVS_penetrance * (1 - self.HVS_damage) * (1 - self.HGS_damage)
#                                     * (1 - self.LGS_damage) * self.LVS_damage)
#                                     * (1 - self.ENV_risk) +
#                 self.ENV_risk )
