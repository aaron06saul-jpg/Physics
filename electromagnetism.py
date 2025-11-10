import numpy as np

time = 1
ticks_per_second = 100
ticks = time*ticks_per_second
time_per_tick = 1/ticks_per_second

class ChargedParticle:
    def __init__(self, charge, mass, velocity, position): # charge and mass are scalars, whereas velocity and position will be lists of 3 numbers
        if not(isinstance(velocity, np.ndarray) and len(velocity) == 3) or not(isinstance(position, np.ndarray) and len(velocity) == 3):
            print("these values are not in the correct form")
            exit()
        self.charge = charge
        self.mass = mass
        self.velocity = velocity 
        self.position = position

    def magnetic_field(self, point): # magnetic field at a specific point - which will be the point of the other point charge
        distance = 0
        vector_distance = np.zeros(3)
        for i in range(3):
            vector_distance[i] = point[i] - self.position[i]
            distance += (vector_distance[i])**2
        distance = distance**(0.5)
        velocity_cross_distance = np.cross(self.velocity, vector_distance)
        magnetic_field = velocity_cross_distance*((self.charge)/((distance)**3))*1e-7
        return magnetic_field
    
    def electric_field(self, point): # same as mag but w electric
        distance = 0
        vector_distance = np.zeros(3)
        for i in range(3):
            vector_distance[i] = point[i] - self.position[i]
            distance += (vector_distance[i])**2
        distance = distance**(0.5)
        electric_field = vector_distance*((self.charge)/(distance)**3)*8.99e9
        return electric_field

particle_A = ChargedParticle(charge=1.6e-9, mass=1.0, velocity=np.array([1.0e3,0.0,0.0]), position=np.array([0.0,0.0,0.0]))
particle_B = ChargedParticle(charge=1.6e-9, mass=1.0, velocity=np.array([0.0,0.0,0.0]), position=np.array([0.0,1.0,0.0]))



def magnetic_force(charge, velocity, magnetic_field):
        force_per_charge = np.cross(velocity, magnetic_field)
        return force_per_charge * charge
    
def electric_force(charge, electric_field):
    return electric_field * charge

positions_A = []
positions_B = []

for i in range(ticks):
    print("particle_A position" + str(particle_A.position))
    print("particle_A velocity" + str(particle_A.velocity))
    print("particle_A position" + str(particle_A.position))
    print("particle_B velocity " + str(particle_B.velocity))
    
    B_field_from_B_at_A = particle_B.magnetic_field(particle_A.position)
    E_field_from_B_at_A = particle_B.electric_field(particle_A.position)

    B_field_from_A_at_B = particle_A.magnetic_field(particle_B.position)  
    E_field_from_A_at_B = particle_A.electric_field(particle_B.position)
    lorentz_acceleration_A = np.add(magnetic_force(particle_A.charge, particle_A.velocity, B_field_from_B_at_A),
    electric_force(particle_A.charge, E_field_from_B_at_A))/(particle_A.mass)
    lorentz_acceleration_B = np.add(magnetic_force(particle_B.charge, particle_B.velocity, B_field_from_A_at_B),
    electric_force(particle_B.charge, E_field_from_A_at_B))/(particle_B.mass)
    particle_A.position += np.add(particle_A.velocity*time_per_tick, lorentz_acceleration_A*(0.5*(time_per_tick**2)))
    particle_B.position += np.add(particle_B.velocity*time_per_tick, lorentz_acceleration_B*(0.5*(time_per_tick**2)))
    particle_A.velocity += lorentz_acceleration_A*time_per_tick
    particle_B.velocity += lorentz_acceleration_B*time_per_tick
    positions_A.append(particle_A.position.copy())
    positions_B.append(particle_B.position.copy())
    
positions_A = np.array(positions_A)
positions_B = np.array(positions_B)