import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.interpolate import interp1d
import csv
import copy


class FitFopdtModel:
    def __init__(self, filename, km, thetam, start_time=0.0, end_time=np.inf):
        # construct initial guess
        self.x0 = np.array([km, thetam])
        self.co = list()  # controller output aka pid sum
        self.pv = list()  # process variable aka gyro data
        self.t = list()  # time stamps
        self.stick = list()  # the stick value aka rcCommand, needed to aid in finding steady state
        # import the data from the cvs file and fill out some of the member variables
        print('Importing data from provided file...')
        self.import_cvs_data(filename, start_time, end_time)

        # solve the model with the initial parameters, this is really just for plotting
        self.ym1 = self.first_order_integrating(self.x0)

    def import_cvs_data(self, filename, starttime, endtime):
        with open(filename, "rb") as theFile:
            reader = csv.DictReader(theFile)
            for line in reader:
                time_stamp = float(line[" time (us)"])
                if starttime <= time_stamp <= endtime:
                    self.co.append(float(line[" axisP[0]"]) + float(line[" axisI[0]"]) + float(line[" axisD[0]"]))
                    self.pv.append(float(line[" gyroADC[0]"]))
                    self.t.append(float(line[" time (us)"]))
                    self.stick.append(float(line[" rcCommand[0]"]))
            self.num_steps = len(self.t)  # the number of samples
            self.pv_0 = self.pv[0]  # the inital measurement (process variable)
            self.t_0  = self.t[0]   # the initial time
            self.co_0 = self.co[0]  # the inital controller output

            # Since there is a dead time, controller output data will need to be interpolated so we can see what it was
            # a certain amount of time in the past.
            self.co_interpolated = interp1d(self.t, self.co)

            # The model is very sensitive to the controller output steady state, it is the controller output required to
            # keep the process variable at zero, in a perfect world it would be zero, but in the real world it is not
            # because either the center of gravity of the quad isn't in the exact center, or maybe one side's motor or
            # esc is stronger than the other side's
            print('Calculating steady state controller output...')
            self.co_ss = self.compute_co_ss()
            print('co_ss = ' + repr(self.co_ss))

    def estimate_model(self):
        # show initial objective
        print('Initial SSE Objective: ' + str(self.objective(self.x0)))
        # optimize Km, thetam
        print('Finding optimized solution...')
        solution = minimize(self.objective, self.x0, method="Nelder-Mead", options={'disp': True})
        x = solution.x

        # show final objective and the optimized parameters
        print('Final SSE Objective: ' + str(self.objective(x)))
        print('Kp: ' + str(x[0]))
        print('thetap: ' + str(x[1]))
        # calculate model with optimized parameters
        self.ym2 = self.first_order_integrating(x)

    def objective(self, x):
        # define the objective function to be minimized
        # simulate model
        ym = self.first_order_integrating(x)
        # if something bad happend in the first_order_integrating function, avoid those numbers by sending infinity
        if ym is False:
            return np.inf
        # calculate objective value using least squares method
        obj = 0.0
        for i in range(len(ym)):
            obj += (ym[i] - self.pv[i]) ** 2
        return obj

    def first_order_integrating(self, x):
        km = x[0]
        thetam = x[1]
        # thetam can't be negative but there isn't a way to bound it in minimize() when using Nelder-Mead
        if thetam < 0:
            return False
        p_v = list()
        p_v.append(self.pv_0)
        for n in range(1, self.num_steps):
            # make sure the time shift from thetam doesn't set us back to before the recording started
            if (self.t[n] - thetam) < self.t_0:
                p_v.append(p_v[n - 1])
            else:
                # reduce multiplications by only doing km x time_delta once
                km_x_time_delta = km*(self.t[n] - self.t[n-1])
                p_v.append(p_v[n-1] + km_x_time_delta * self.co_interpolated(self.t[n] - thetam) - km_x_time_delta*self.co_ss)
        return p_v

    def compute_co_ss(self, allowable_deviation_percentage=1.0):
        # steady state is going to be during a time when the stick is at zero, look for those times but allow a little
        # deviation from zero to account for noise, default is + or - 1%
        range_of_stick = abs(max(self.stick) - min(self.stick))
        upper_bound = allowable_deviation_percentage/100.0 * range_of_stick
        lower_bound = -1 * upper_bound
        ss_clusters = list()  # keep a list of continous clusters that are in the range
        cluster = list()
        for j in range(self.num_steps):
            if lower_bound <= self.stick[j] <= upper_bound:
                cluster.append(j)
            else:
                if len(cluster) != 0:
                    ss_clusters.append(copy.copy(cluster))
                    del cluster[:]
        max_cluster_len = 0
        largest_cluster_index = 0
        for k in range(len(ss_clusters)):
            if len(ss_clusters[k]) > max_cluster_len:
                max_cluster_len = len(ss_clusters[k])
                largest_cluster_index = k
        ss_cluster = ss_clusters[largest_cluster_index]
        ss_co_values = list()
        for d in ss_cluster:
            ss_co_values.append(self.co[d])
        return np.mean(ss_co_values)

    def plot_results(self, plot_output=True):
        print "plotting results..."
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.t, self.ym1, 'b-', linewidth=2, label='Initial Guess')
        plt.plot(self.t, self.pv, 'k-', linewidth=2, label='Recorded Data')
        if plot_output:
            plt.plot(self.t, self.ym2, 'r--', linewidth=3, label='Optimized FOPDT')
        plt.axhline(0.0)
        plt.ylabel('Gyro (raw units)')
        plt.legend(loc='best')
        plt.subplot(2, 1, 2)
        plt.plot(self.t, self.co, 'b-', linewidth=2)
        plt.axhline(0.0)
        plt.ylabel('PID_sum (raw units)')
        plt.xlabel('time (us)')
        plt.show()

if __name__ == '__main__':
    fopdt = FitFopdtModel('./test_data/4sflights3.04_edited.csv', .0015, 20000.0, 55200000.0, 55901500.0)
    fopdt.estimate_model()
    fopdt.plot_results()
