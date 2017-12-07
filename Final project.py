import numpy
import random
import pylab as pl

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
             Initialize a SimpleVirus instance, saves all parameters as attributes
             of the instance.
             maxBirthProb: Maximum reproduction probability (a float between 0-1)
             clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb=maxBirthProb
        self.clearProb=clearProb


    def doesClear(self):
        """
             Stochastically determines whether this virus is cleared from the
             patient's body at a time step.
             returns: Using a random number generator (random.random()), this method
             returns True with probability self.clearProb and otherwise returns
             False.
        """
        if random.random() <= self.clearProb:
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
             Stochastically determines whether this virus particle reproduces at a
             time step. Called by the update() method in the SimplePatient and
             Patient classes. The virus particle reproduces with probability
             self.maxBirthProb * (1 - popDensity).

             If this virus particle reproduces, then reproduce() creates and returns
             the instance of the offspring SimpleVirus (which has the same
             maxBirthProb and clearProb values as its parent).

             popDensity: the population density (a float), defined as the current
             virus population divided by the maximum population.

             returns: a new instance of the SimpleVirus class representing the
             offspring of this virus particle. The child should have the same
             maxBirthProb and clearProb values as this virus. Raises a
             NoChildException if this virus particle does not reproduce.
        """
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()

class SimplePatient(object):
    """
         Representation of a simplified patient. The patient does not take any drugs
         and his/her virus populations have no drug resistance.
    """
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as attributes.
        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses=viruses
        self.maxPop=maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population.
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
        value is used until the next call to update()

        - Determine whether each virus particle should reproduce and add
        offspring virus particles to the list of viruses in this patient.
        returns: the total virus population at the end of the update (an
        integer)
        """
        for i in range(len(self.viruses)-1, -1, -1):
            if self.viruses[i].doesClear():
                self.viruses.pop(i)
        current_popDensity=self.getTotalPop()/self.maxPop
        for virus in self.viruses:
            try:
                self.viruses.append(virus.reproduce(current_popDensity))
            except NoChildException:
                pass
        return self.getTotalPop()

class NoChildException(Exception):
    """
    a NoChildException indicating that the virus particle does not reproduce during the current time step.
    """
    pass

def problem2():
    """
        Run the simulation and plot the graph for problem 2 (no drugs are used,
        viruses do not have any drug resistance).
        Instantiates a patient, runs a simulation for 300 timesteps, and plots the
        total virus population as a function of time.
    """
    len_viruses=100
    maxPop=1000
    maxBirthProb=0.1
    clearProb=0.05
    timesteps=300
    single_virus=SimpleVirus(maxBirthProb,clearProb)
    viruses=[]
    for i in range(len_viruses):
        viruses.append(single_virus)
    single_patient=SimplePatient(viruses,maxPop)
    #initial state
    x_time=[0]
    y_pop=[100]
    for i in range(1,timesteps+1):
        x_time.append(i)
        y_pop.append(single_patient.update())
    pl.plot(x_time,y_pop)
    pl.xlabel("time step")
    pl.ylabel("virus population")
    pl.title("Simulating Virus Population Dynamics without Drug Treatment")
    pl.show()

#problem2()


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.
        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.
        drug: the drug (a string).
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if self.resistances[drug] == True:
            return True
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability: self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population
        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        resist = False
        if activeDrugs:
            for drug in activeDrugs:
                if self.getResistance(drug):
                    resist = True
                    break
        else:
            resist = True

        if resist:
            if random.random() <= (self.maxBirthProb * (1 - popDensity)):
                newresistances = {}
                for drug in self.resistances.keys():
                    if random.random() <= (1 - self.mutProb):
                        newresistances[drug] = self.resistances[drug]
                    else:
                        newresistances[drug] = not self.resistances[drug]
                return ResistantVirus(self.maxBirthProb, self.clearProb, newresistances, self.mutProb)
            else:
                raise NoChildException()
        else:
            raise NoChildException()


class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her virus population
    can acquire resistance to the drugs he/she takes.
    """
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).
        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses=viruses
        self.maxPop=maxPop
        self.administered=[]

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.
        newDrug: The name of the drug to administer to the patient (a string).
        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.administered:
            self.administered.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.administered

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in drugResist.
        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])
        returns: the population of viruses (an integer) with resistances to all drugs in the drugResist list.
        """
        notresist_pop=0
        for virus in self.viruses:
            for drug in drugResist:
                if virus.getResistance(drug)== False:
                    notresist_pop=notresist_pop +1
                    break
        resist_pop=len(self.viruses)-notresist_pop
        return resist_pop

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        - Determine whether each virus particle survives and update the list of virus particles accordingly
        - The current population density is calculated. This population density value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add offspring virus particles to the list of viruses in this patient.
        The list of drugs being administered should be accounted for in the determination of whether each virus particle reproduces.
        returns: the total virus population at the end of the update (an integer)
        """
        for i in range(len(self.viruses) - 1, -1, -1):
            if self.viruses[i].doesClear():
                self.viruses.pop(i)
        current_popDensity = len(self.viruses) / self.maxPop
        for virus in self.viruses:
            try:
                self.viruses.append(virus.reproduce(current_popDensity, self.administered))
            except NoChildException:
                pass
        return self.getTotalPop()


def problem4():
    """
         Runs simulations and plots graphs for problem 4.
         Instantiates a patient, runs a simulation for 150 timesteps, adds
         guttagonol, and runs the simulation for an additional 150 timesteps.
         total virus population vs. time  and guttagonol-resistant virus population
         vs. time are plotted
    """
    len_viruses = 100
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False}
    mutProb = 0.005
    timesteps = 300
    resistant_virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    viruses = []
    for i in range(len_viruses):
        viruses.append(resistant_virus)
    single_patient = Patient(viruses, maxPop)

    x_time = [0]
    y_pop = [100]
    y_pop_resistant = [0]
    for i in range(1, timesteps + 1):
        x_time.append(i)
        y_pop.append(single_patient.update())
        y_pop_resistant.append(single_patient.getResistPop(['guttagonol']))
        if i == 150:
            single_patient.addPrescription("guttagonol")

    pl.plot(x_time, y_pop,label="Total virus population")
    pl.plot(x_time, y_pop_resistant,label="guttagonol-resistant population")
    pl.xlabel("time step")
    pl.ylabel("virus population")
    pl.title("Simulating Virus Population Dynamics with Drug Treatment")
    pl.legend()
    pl.show()

#problem4()

def problem5():
    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,150, 75, 0 timesteps
    (followed by an additional 150 timesteps of simulation).
    """
    patientsnum = 200
    len_viruses = 100
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False}
    mutProb = 0.005
    timesteps = 150
    resistant_virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    delay_timesteps=[300,150,75,0]
    for delaytime in delay_timesteps:
        y_pop_total = []
        cured_num=0
        for i in range(patientsnum):
            viruses = []
            for j in range(len_viruses):
                viruses.append(resistant_virus)
            single_patient = Patient(viruses, maxPop)
            #y_pop = [100]
            for m in range(delaytime + timesteps):
                y_pop = single_patient.update()
                if m == delaytime:
                    single_patient.addPrescription("guttagonol")
            y_pop_total.append(y_pop)
            if y_pop<=50:
                cured_num=cured_num+1
        cured_prob=cured_num/patientsnum
        pl.hist(y_pop_total)
        pl.title(str(cured_prob*100) + "% of patients were cured when the drug added after " + str(delaytime) + " timesteps")
        pl.xlabel('Total virus populations')
        pl.ylabel('Number of patients')
        pl.show()

#problem5()


def problem6():
    """
         Runs simulations and make histograms for problem 6.
         Runs multiple simulations to show the relationship between administration
         of multiple drugs and patient outcome.
         Histograms of final total virus populations are displayed for lag times of
         150, 75, 0 timesteps between adding drugs (followed by an additional 150
         timesteps of simulation).
    """
    patientsnum = 30
    len_viruses = 100
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False, 'grimpex':False}
    mutProb = 0.005
    timesteps = 150
    resistant_virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    lag_timesteps = [300, 150, 75, 0]
    for lagtime in lag_timesteps:
        y_pop_total = []
        cured_num = 0
        for i in range(patientsnum):
            viruses = []
            for j in range(len_viruses):
                viruses.append(resistant_virus)
            single_patient = Patient(viruses, maxPop)
            # y_pop = [100]
            for m in range(timesteps + lagtime + timesteps):
                y_pop = single_patient.update()
                if m == timesteps:
                    single_patient.addPrescription("guttagonol")
                if m == (timesteps+lagtime):
                    single_patient.addPrescription("grimpex")
            y_pop_total.append(y_pop)
            if y_pop <= 50:
                cured_num = cured_num + 1
        print(y_pop_total)
        cured_prob = cured_num / patientsnum
        pl.hist(y_pop_total)
        pl.title(str(cured_prob * 100) + "% of patients were cured when the interval of two drugs is " + str(lagtime) + " timesteps")
        pl.xlabel('Total virus populations')
        pl.ylabel('Number of patients')
        pl.show()

#problem6()

def problem7():
    """
         Run simulations and plot graphs examining the relationship between
         administration of multiple drugs and patient outcome.
         Plots of total and drug-resistant viruses vs. time are made for a
         simulation with a 300 time step delay between administering the 2 drugs and
         a simulations for which drugs are administered simultaneously.
    """
    #150-300-150
    len_viruses = 100
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False, 'grimpex': False}
    mutProb = 0.005
    timesteps = 150
    lag_time=300
    resistant_virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
    viruses = []
    for j in range(len_viruses):
        viruses.append(resistant_virus)
    single_patient = Patient(viruses, maxPop)
    y_pop = []
    resist_gut = []
    resist_gri = []
    resist_all = []
    for m in range(timesteps+lag_time+timesteps):
        y_pop.append(single_patient.update())
        resist_gut.append(single_patient.getResistPop(['guttagonol']))
        resist_gri.append(single_patient.getResistPop(['grimpex']))
        resist_all.append(single_patient.getResistPop(['guttagonol', 'grimpex']))
        if m == timesteps:
            single_patient.addPrescription("guttagonol")
        if m == (timesteps + lag_time):
            single_patient.addPrescription("grimpex")
    pl.plot(y_pop,label = 'Total virus population')
    pl.plot(resist_gut,label = 'guttagonol-resistant')
    pl.plot(resist_gri,label = 'grimpex-resistant')
    pl.plot(resist_all,label = 'all-resistant')
    pl.xlabel('virus populations')
    pl.ylabel('Number of patients')
    pl.legend()
    pl.show()

    #150-150
    viruses = []
    for j in range(len_viruses):
        viruses.append(resistant_virus)
    single_patient = Patient(viruses, maxPop)
    y_pop = []
    resist_gut = []
    resist_gri = []
    resist_all = []
    for m in range(timesteps+timesteps):
        y_pop.append(single_patient.update())
        resist_gut.append(single_patient.getResistPop(['guttagonol']))
        resist_gri.append(single_patient.getResistPop(['grimpex']))
        resist_all.append(single_patient.getResistPop(['guttagonol', 'grimpex']))
        if m == timesteps:
            single_patient.addPrescription("guttagonol")
            single_patient.addPrescription("grimpex")
    pl.plot(y_pop, label='Total virus population')
    pl.plot(resist_gut, label='guttagonol-resistant')
    pl.plot(resist_gri, label='grimpex-resistant')
    pl.plot(resist_all, label='all-resistant')
    pl.xlabel('Total virus populations')
    pl.ylabel('Number of patients')
    pl.legend()
    pl.show()

#problem7()