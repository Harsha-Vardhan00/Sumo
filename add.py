import os
import sys
import optparse

if "SUMO_HOME" in os.environ:

    tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME")

from sumolib import checkBinary #Checks for the binary in environ vars Amorz Kraci
import traci
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="Run the commandline version of SUMO")
    options, args = opt_parser.parse_args()
    return options

#contains TraCI control loop

def run():
    step = 0
    while True:
        traci.simulationStep()
        step += 1
        print("Step:", step)
        
        # Add the new vehicle at step 10
        if step == 2:
            traci.vehicle.add("ce22b118", "r_0", depart=str(step), departLane="first", departPos="base", departSpeed='0', arrivalLane='current', arrivalPos='max', arrivalSpeed='current', fromTaz='', toTaz='', line='', personCapacity=0, personNumber=0)
    step = 0
    while True:
        traci.simulationStep()
        step += 1
        print("Step:", step)
        # Get the position and velocity of the SUMO vehicle
        leader_pos = traci.vehicle.getPosition("t_0")
        leader_velocity = traci.vehicle.getSpeed("t_0")
        
        # Get the position of the new vehicle
        follower_pos = traci.vehicle.getPosition("ce22b118")
        
        # Calculate the distance between the vehicles
        distance = abs(leader_pos[0] - follower_pos[0])
        
        # Calculate the desired gap
        desired_gap = 2.5
        
        # If the distance is less than the desired gap, slow down the new vehicle
        if distance < desired_gap:
            new_velocity = max(0, leader_velocity - (desired_gap - distance))
        else:
            new_velocity = leader_velocity
        
        # Set the velocity for the new vehicle
        traci.vehicle.setSpeed("ce22b118", new_velocity)
            
        # Process additional logic or user input here
        
        # Exit loop when there are no more vehicles in the simulation
        if not traci.simulation.getMinExpectedNumber():
            break
 # Exit loop when there are no more vehicles in the simulation



    traci.close() 
    sys.stdout.flush()

#main entry point
if __name__ == '__main__':

    options=get_options()
    if options.nogui:
        sumoBinary=checkBinary("sumo")

    else:
        sumoBinary=checkBinary('sumo-gui')
    traci.start([sumoBinary,"-c","sumo.sumocfg","--tripinfo-output","tripinfo.xml"])
    run()

#traci starts sumo as a subprocess and then this script connects and runs traci.start((sum Binary, c", "dumo sumesia". trisinfo-output", "tripinfo.xml")














