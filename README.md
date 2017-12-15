# Title: Simulation of virus population dynamics

## Team Member(s):Huidan Xiao & Siti Zhang

# Monte Carlo Simulation Scenario & Purpose:
It's a big challenge for the modern medicine to charm off some viruses due to their ability to evolve. When the human is infected with the virus, the virus must rely on the growth of human cells to reproduce and thus avoiding the elimination of immune mechanism. Although there are some drugs for virus treatment, they can only inhibit the reproduction of the virus, minimize the number of viruses, and reduce the harm of the virus to the human body. For example, in terms of the HIV treatment, cocktail therapy can reduce the drug resistance of a single drug and maximize the inhibition of viral replication. Therefore, it is important to understand the virus population dynamics in a patient.

In this project, we will first simulate the virus population dynamics without drug treatment. Then we not only analyze the effects of drugs on patients, but also understand the changes in the virus population during drug treatment and their resistance to drug after inheritance or mutation. Finally, we will analyze the effect of delaying treatment on the ability of the drug to eradicate the virus population and decide the best way of administering the two drugs. The purpose of the study is to explore the effects of drug therapy on the virus population and determine a better way to improve the cure rate of drugs treatment.

### Hypothesis before running the simulation:
H1: The probability of a virus particle being cleared is constant at every time step of the simulation.

H2: The probability of a virus particle reproducing is a function of the virus population. 

reproduce_virus = self.maxBirthProb * ( 1 - popDensity)

self.maxBirthProb is the birth rate under optimal conditions (the virus population is negligible relative to the available host cells). popDensity is defined as the ratio of the current virus population to the maximum virus population for a patient.

H3: The effect of drugs on the virus is not to clear the virus directly, but to prevent reproduction.
### Simulation's variables of uncertainty
List and describe your simulation's variables of uncertainty (where you're using pseudo-random number generation). 
For each such variable, how did you decide the range and which probability distribution to use?  
Do you think it's a good representation of reality?
Variables of uncertainty:

1.Virus Reproduce Probability.

reproduce_virus = self.maxBirthProb * ( 1 - popDensity)

With virus population increasing, the virus reproduce probability will decrease.

2.Virus Population

The amount of whole virus.The virus population can be decided by which random group of virus reproduce , which random virus group have resistance to a drug and which random virus group will have mutation to gain or lose resistance to a drug. As for the range of virus population in a patient, it is set to 1000, and each random simulation will carry uniform distribution.

3.PopDensity

The ratio of the current virus population to the maximum virus population for a patient.

Fixed variables: 

1.maxPop

maximum virus population for a patient.  1000

2.maxBirthProb 

The virus birthrate under optimal conditions. 100，0.8———>80

3.clearProb

Maxium clearance probability of a virus particle, 100, 0.1———>10

4.mutProb

Mutation probability of a virus,100,0.05———>5

## Instructions on how to use the program:

Only simple virus in simple Patient

SimplePatient():

Update (). ------doesclear(). Decide which are cleared and which are survive

|                         

Reproduce()----------- foreachvirus to reproduce(each virus ----> SimpleVirus)

|            \

|             NoChildException()  the virus does not reproduce during the current time stamp

Return a new virus instance as the offspring of the virus 

|

Update()

 

Add drug to patient

GetPrescription()———-to return the drugs that are being administered to this patient.

|

AddPresciption()———add new drug to this patient

|

GetResistance()————to test each virus to see if they are resistant to a drug(———>ResistantVirus)

|

GetResistPop()—————to return all the virus that are resistant to all the drugs

|

Update()
## Sources Used:
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00-introduction-to-computer-science-and-programming-fall-2008/assignments/pset12.pdf

