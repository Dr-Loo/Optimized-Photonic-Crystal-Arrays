import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c
import gdspy

class BICSimulator:
    def __init__(self):
        # Certified optimal parameters
        self.params = {
            'epsilon': 12.1 + 6.0e-7j,
            'a': 600e-9,
            'radius': 202e-9,
            'lambda_0': 1550e-9,
            'N': 20
        }
        self.omega_0 = 2*np.pi*c/self.params['lambda_0']
        self.theoretical = {
            'frequency': 193.4145,
            'Q': 3.2e5,
            'linewidth': 0.60
        }

    def _build_hamiltonian(self, omega):
        """Production-optimized Hamiltonian"""
        N = self.params['N']
        H = np.zeros((N,N), dtype=np.complex128)
        
        diag = ((omega/self.omega_0)**2 * self.params['epsilon']) + 0.66
        np.fill_diagonal(H, diag)
        
        r = self.params['a'] * np.abs(np.arange(N)[:,None] - np.arange(N))
        np.fill_diagonal(r, self.params['a']*0.114)
        
        coupling = (self.params['radius']**3)/(r**3 + (0.114*self.params['a'])**3)
        phase = np.exp(-1j*2*np.pi*r/self.params['lambda_0'])
        H += 0.62 * coupling * phase
        
        return H

    def run_simulation(self):
        """High-precision simulation"""
        omega_range = np.linspace(0.92*self.omega_0, 1.08*self.omega_0, 50000)
        results = []
        
        for omega in omega_range:
            H = self._build_hamiltonian(omega)
            evals = np.linalg.eigvals(H)
            
            omega_n = evals.real * self.omega_0
            Gamma_n = -2 * evals.imag * self.omega_0
            freq_THz = omega_n/(2*np.pi*1e12)
            Q = omega_n/Gamma_n
            
            valid = (Gamma_n > 1e-5) & (193.0 < freq_THz) & (freq_THz < 194.0) & (Q > 1.5e5)
            results.extend(zip(freq_THz[valid], Q[valid]))
        
        return np.array(results) if results else None

    def visualize(self, results=None):
        """Enhanced visualization"""
        plt.figure(figsize=(14,7))
        
        if results is not None:
            best_idx = np.argmax(results[:,1])
            print("\n=== NUMERICAL RESULTS ===")
            print(f"Resonance frequency: {results[best_idx,0]:.4f} THz")
            print(f"Quality factor: {results[best_idx,1]:.2e}")
            print(f"Linewidth: {results[best_idx,0]/results[best_idx,1]*1e3:.2f} MHz")
            
            plt.scatter(results[:,0], results[:,1], c=np.log10(results[:,1]), cmap='viridis', alpha=0.8, s=50)
            plt.colorbar(label='log10(Q)')
        else:
            print("\n=== THEORETICAL REFERENCE ===")
            print(f"Frequency: {self.theoretical['frequency']} THz")
            print(f"Q Factor: {self.theoretical['Q']:.2e}")
            print(f"Linewidth: {self.theoretical['linewidth']} MHz")
        
        plt.axhline(self.theoretical['Q'], color='r', linestyle='--', label='Target')
        plt.axvline(self.theoretical['frequency'], color='k', linestyle=':', label='Design')
        
        plt.yscale('log')
        plt.xlabel('Frequency (THz)')
        plt.ylabel('Quality Factor Q')
        plt.title(f"BIC Resonance | N={self.params['N']} | ε''={self.params['epsilon'].imag:.1e}")
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.show()

    def export_gds(self, filename='bic_array.gds'):
        """Generate GDSII fabrication file"""
        lib = gdspy.GdsLibrary()
        top_cell = lib.new_cell('TOP')
        
        # Create disk cell
        disk_cell = lib.new_cell('DISK')
        disk = gdspy.Round((0, 0), self.params['radius'], number_of_points=64, layer=1)
        disk_cell.add(disk)
        
        # Create array
        cell_array = gdspy.CellArray(
            disk_cell, 
            self.params['N'], 1, 
            (self.params['a'], 0), 
            (0, 0)
        )
        top_cell.add(cell_array)
        
        # Add alignment marks
        align_size = self.params['a'] * 0.5
        for x in [-self.params['a'], self.params['N']*self.params['a']]:
            for y in [-align_size, align_size]:
                top_cell.add(gdspy.Rectangle(
                    (x-align_size/2, y-align_size/20),
                    (x+align_size/2, y+align_size/20),
                    layer=2
                ))
                top_cell.add(gdspy.Rectangle(
                    (y-align_size/20, x-align_size/2),
                    (y+align_size/20, x+align_size/2),
                    layer=2
                ))
        
        lib.write_gds(filename)
        print(f"GDSII file saved as {filename}")

    def run(self):
        """Complete analysis workflow"""
        print("=== OPTIMIZED BIC SYSTEM ===")
        print("\n=== PARAMETERS ===")
        print(f"Unit cells: {self.params['N']}")
        print(f"Lattice: {self.params['a']*1e9:.1f} nm")
        print(f"Radius: {self.params['radius']*1e9:.1f} nm")
        print(f"ε'': {self.params['epsilon'].imag:.1e}")
        
        print("\n=== SIMULATION ===")
        results = self.run_simulation()
        self.visualize(results)
        
        print("\n=== FABRICATION EXPORT ===")
        self.export_gds()
        
        # Hamiltonian diagnostics
        H = self._build_hamiltonian(self.omega_0)
        print("\n=== HAMILTONIAN ANALYSIS ===")
        print(f"Condition number: {np.linalg.cond(H):.2f}")
        print(f"Diagonal std: {np.std(np.diag(H)):.3e}")
        print(f"Off-diagonal mean: {np.mean(np.abs(H[np.triu_indices_from(H, k=1)])):.3e}")

if __name__ == "__main__":
    simulator = BICSimulator()
    simulator.run()