import math
class Auction:
      def __init__(self):
            self.location=[[100,200,40],[120,300,50],[300,100,45]]   # coordinates of each UAV (x,y,z)
            self.cost_of_UAV=[10,18,8]                          
            self.satisfaction_parameter = [ 0.5,0.75,1.5]          # satisfaction parameter
            self.wgn= 1e-4                                       # White Guassian Parameter
            self.B0 = -50                                        # UAV_to_ground channel gain 
            self.transmission_power = 0.5                        # transmission_power for both UAV and Base station
            self.unit_distance = -2                              # path loss parameter                    
            self.data_rate =[14,8,12]                              # data-rate demand of CSP
            self.UAV_bandwidth = [10,13,8]                      # Each UAV initial Bandwidth
            # self.UAV_price = [20,30,25,36,41]                  # Each UAV initial Price -> pm(t)
            self.user_required_bandwidth = [0,0,0]
            self.power_gain = [12,25,18]                         #power_gain from BS->CSP
          
      def distance(self,location_xyz):
            return math.sqrt(location_xyz[0]**2 + location_xyz[1]**2 + location_xyz[2]**2)
 
      def channel_gain(self, location_xyz):
             return (self.B0*self.distance(location_xyz))**self.unit_distance
 
      def unit_bandwidth_data_rate(self, cost_of_UAV, location_xyz):
            return math.log2(1+self.SINR(cost_of_UAV, location_xyz))
      
      def SINR(self, cost_of_UAV,location_xyz):
            sum_gain =0;
            for i in range(len(cost_of_UAV)):
                  sum_gain += self.transmission_power * self.channel_gain(self.location[i])
                  # sum_gain += (cost_of_UAV[i]*self.channel_gain(self.location[i]) + self.transmission_power*self.power_gain[i])
                  
            signal_ratio = (self.transmission_power*self.channel_gain(location_xyz))/(self.wgn+sum_gain+ self.transmission_power*self.power_gain[i])
            return signal_ratio
        
      def total_UAV_bandwidth(self, UAV_bandwidth):
            total_bandwidth = 0
            for i in range(len(UAV_bandwidth)):
                  total_bandwidth = total_bandwidth + UAV_bandwidth[i]
            return total_bandwidth

      def gradient_utility(self, cost_of_UAV):
            n = len(cost_of_UAV)
            Utility =0
            for i in range(n):
                  x = (self.cost_of_UAV[i]*self.satisfaction_parameter[i])/(cost_of_UAV[i]*cost_of_UAV[i])
                  y = (self.data_rate[i])/(self.unit_bandwidth_data_rate(self.cost_of_UAV,self.location[i]))
                  Utility = Utility + (x-y)
            return Utility
      
      def new_user_requirement(self):
            for i in range(len(self.cost_of_UAV)):
                  x = self.satisfaction_parameter[i]/self.cost_of_UAV[i]
                  y = self.data_rate[i]/self.unit_bandwidth_data_rate(self.cost_of_UAV,self.location[i])
                  self.user_required_bandwidth[i] = max(0,(x - y))

      def total_requirement(self, user_required_bandwidth):
            total_bandwidth_requirement = 0
            for i in range(len(user_required_bandwidth)):
                  total_bandwidth_requirement = total_bandwidth_requirement + user_required_bandwidth[i]
            return total_bandwidth_requirement
      
      def run(self):
            UAV_total_bandwidth = self.total_UAV_bandwidth(self.UAV_bandwidth)   # Total bandwidth (B0)
            
            self.new_user_requirement()    # Finding bn(tm) w.r.t user satisfaction_parameter and UAV price
            
            print("\nUser Bandwidth Requirement: "+str(self.user_required_bandwidth))
            iteration = 0
            print("UAV_bandwidth: " + str(self.UAV_bandwidth))
            print("Initial Price: "+str(self.cost_of_UAV))
            while(iteration<10):
                  # Cellular service provider within the coverage of each UAV determines their bandwidth requirements
                  # Hence Total requirement of CSP
                  total_bandwidth_requirement = self.total_requirement(self.user_required_bandwidth)  
                  if total_bandwidth_requirement > UAV_total_bandwidth:
                        for i in range(len(self.cost_of_UAV)):
                              self.cost_of_UAV[i] = self.cost_of_UAV[i] + 2
                  else:
                        for i in range(len(self.cost_of_UAV)):
                              x = self.gradient_utility(self.cost_of_UAV)
                              self.cost_of_UAV[i] = self.cost_of_UAV[i] + x
                  iteration = iteration+1
                  
            
            print("UAV_price: " + str(self.cost_of_UAV))
                        
a = Auction()

a.run()