"""
This code simulates the motion of a two-filament scallop. 
The hydrodynamic interactions between the two filaments are taken into account. 
The model oscillates and does not generate a net swimming motion.
"""
import numpy as np
from scipy.linalg import solve
from gaussxw import gaussxw, rescale

def stokeslet_reg(rsr, rtar, delta):
    """
    Regularized Stokeslet
    rsr: source position, (3,N)
    rtar: target point, (3,1)
    delta: regularization parameter
    
    Return:
    G, (3,3,N)
    """
    N = rsr.shape[1]

    R = rtar - rsr # (3, N)
    Rsquare = np.sum(R**2, axis=0) # (N,)
    Rabs_reg = np.sqrt(Rsquare + delta**2) # (N,)

    I = np.identity(3)
    G = np.zeros((3,3,N))
    for i in range(3):
        for j in range(3):
            G[i,j,:] = (Rsquare+2*delta**2)/Rabs_reg**3*I[i,j] + R[i,:]*R[j,:]/Rabs_reg**3

    G = G/(8*np.pi)

    return G

class TwoFilamentScallop:
    def __init__(self, theta_A, theta_0, N, L, dt, T, tau, delta, nfine):
        # Physical parameters
        self.theta_A = theta_A # amplitude
        self.theta_0 = theta_0 # tilting angle
        self.N = N # number of discrete segments
        self.L = L # filament length
        self.dt = dt # time step
        self.T = T # simulation duration
        self.tau = tau # oscillation period
        self.delta = delta # regularization parameter
        self.nfine = nfine # number of Gauss–Legendre points
        
        # arclength discretization
        self.ds = L / N
        self.s = np.linspace(-L/2, L/2, N+1)
        self.s_mid = (self.s[:-1] + self.s[1:]) / 2.0
        
        # Gaussian quadrature
        self.nodes, self.weights = gaussxw(nfine)
        
        # Filament arrays
        self.r1 = np.zeros((N, 3))  # Upper filament positions
        self.r2 = np.zeros((N, 3))  # Lower filament positions
        
        # Hinged points
        self.x_hinge = 0.
        self.r_hinge1 = np.array([self.x_hinge, 5*delta, 0.0])
        self.r_hinge2 = np.array([self.x_hinge, -5*delta, 0.0])
        
        # System matrices
        self.lhs = np.zeros((3*N+1, 3*N+1))
        self.rhs = np.zeros(3*N+1)
        
        self.t = 0.0
        self.U = 0.0

        # Initialize geometry
        self.update_geometry()

    def update_geometry(self):
        """Update filament angles and positions"""
        # Update orientation angles
        self.theta1 = self.theta_A * np.sin(2*np.pi*self.t/self.tau) + self.theta_0
        self.theta1_dot = self.theta_A * (2*np.pi/self.tau) * np.cos(2*np.pi*self.t/self.tau)
        self.theta2 = -self.theta1
        self.theta2_dot = -self.theta1_dot
        
        # tangent vectors
        self.p1 = np.array([np.cos(self.theta1), np.sin(self.theta1), 0.0])
        self.p2 = np.array([np.cos(self.theta2), np.sin(self.theta2), 0.0])
        
        # Update hinged positions
        self.r_hinge1[0] = self.x_hinge
        self.r_hinge2[0] = self.x_hinge
        
        # Update filament positions
        for i in range(self.N):
            self.r1[i] = self.r_hinge1 + (self.s_mid[i] + self.L/2) * self.p1
            self.r2[i] = self.r_hinge2 + (self.s_mid[i] + self.L/2) * self.p2

    def get_gauss_points(self, element_idx, fila_id):
        """Get Gauss–Legendre points"""
        s_start, s_end = self.s[element_idx], self.s[element_idx+1]
        ss, w = rescale(self.nodes, self.weights, s_start, s_end)
        
        if fila_id == 1:
            hinge = self.r_hinge1
            tang = self.p1
        else:
            hinge = self.r_hinge2
            tang = self.p2
        
        positions = np.zeros((3, self.nfine))
        for k in range(self.nfine):
            positions[:, k] = hinge + (ss[k] + self.L/2) * tang
            
        return positions, w

    def form_linear_system(self):
        """Construct linear system for BEM"""
        self.lhs.fill(0)
        self.rhs.fill(0)
        
        # Mirror symmetry transformation
        M_mirror = np.diag([1.0, -1.0, 1.0])
        
        # Form hydrodynamic interactions
        for i in range(self.N):
            target_pos = self.r1[i].reshape(3, 1)
            
            # Self-interaction: filament 1 on itself
            for j in range(self.N):
                source_pos, weights = self.get_gauss_points(j, 1)
                G = stokeslet_reg(source_pos, target_pos, self.delta)
                self.lhs[3*i:3*i+3, 3*j:3*j+3] += np.sum(G * weights, axis=2)
            
            # Cross-interaction: filament 2 on filament 1
            for j in range(self.N):
                source_pos, weights = self.get_gauss_points(j, 2)
                G = stokeslet_reg(source_pos, target_pos, self.delta)
                self.lhs[3*i:3*i+3, 3*j:3*j+3] += np.sum(G * weights, axis=2) @ M_mirror
            
            # Prescribed rotational velocity
            v_rot = (self.s_mid[i] + self.L/2) * self.theta1_dot
            self.rhs[3*i] = v_rot * (-np.sin(self.theta1))
            self.rhs[3*i+1] = v_rot * np.cos(self.theta1)
            self.rhs[3*i+2] = 0.0
        
        # Translation velocity
        for i in range(self.N):
            self.lhs[3*i, 3*self.N] = -1.0

        # Force-free condition
        for i in range(self.N):
            self.lhs[3*self.N, 3*i] = self.ds

    def solve_system(self):
        """Solve linear system"""
        results = solve(self.lhs, self.rhs)
        self.U = results[3*self.N]
        
        # Update hinged position
        self.x_hinge += self.U * self.dt

    def step(self):
        """Execute one time step"""
        self.update_geometry()
        self.form_linear_system()
        self.solve_system()

    def simulate(self, filename="scallop_results.txt", savedata=True):
        """Run complete simulation"""
        if savedata:
            fileobj = open(filename, "w")
        
        while self.t < self.T:
            print("{:.2f}".format(self.t))
            self.step()
            
            if savedata:
                fileobj.write("{:.5f} {:.10f} {:.10f}\n".format(self.t, self.U, self.x_hinge))
                fileobj.flush()
            
            self.t += self.dt
        
        if savedata:
            fileobj.close()
            print(f"Results saved to {filename}")

if __name__ == "__main__":
    theta_A = 1.0 # oscillation amplitude
    theta_0 = 1.0 # tilting angle
    N = 100 # number of discrete segments
    L = 1.0  # filament length
    dt = 0.002 # time step
    T = 1.0 # simulatio duration
    tau = 1.0 # oscillation period
    delta = 0.01 # regularization parameter
    nfine = 6 # number of Gauss–Legendre points
    
    # Create and run simulation
    # theta_A, theta_0, N, L, dt, T, tau, delta, nfine
    sim = TwoFilamentScallop(theta_A, theta_0, N, L, dt, T, tau, delta, nfine)
    sim.simulate(savedata=True)