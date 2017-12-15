
import urllib.request
import sys
import json
import copy

class Tour:
    
    def __init__(self, *args):
        self.cities = []
        self.states = []
        self.mode = "driving"
        for arg in args:
            pairs= arg.split(",")
            if len(pairs)!=2:
                print("Check the cities you want to travel!!!!! They are ill formed.........So, I am  quiting!!!")
                sys.exit(1)
            self.cities.append(pairs[0].strip())
            self.states.append(pairs[1].strip())

    def __str__(self):
        ret_value = ""
        for i in range(len(self.cities)):
            ret_value += "\"" +self.cities[i] + "," + self.states[i] + "\"" 
            if i != (len(self.cities)-1):
                ret_value += ","
        return ret_value+self.mode

    def __repr__(self):
        ret_value = ""
        for i in range(len(self.cities)):
            ret_value += "\"" +self.cities[i] + "," + self.states[i] + "\"" 
            if i != len(self.cities):
                ret_value += ","
        return ret_value

    def distance(self, mode="driving"):
        self.mode = mode
        i = 0
        total_distance = 0
        while ( i< (len(self.cities)-1) ):
            result = self.one_hop_distance((self.cities[i]+","+self.states[i]), (self.cities[i+1]+","+self.states[i+1]))
            index_of_value = result.index("value\" : ")+9
            index_of_bracket = result.index("\\n", index_of_value)
            value = float(result[index_of_value:index_of_bracket].strip())
            #print("i th hop distance is ", value)
            total_distance += value
            i = i+1
        total_distance = total_distance  
        return total_distance
        
    def one_hop_distance(self, origin, destination):
        server_address_as_string = "http://maps.googleapis.com/maps/api/distancematrix/json?origins="
        query_string = server_address_as_string + origin.strip().replace(" ","+").replace(",","+")
        query_string = query_string + "&destinations="+ destination.strip().replace(" ","+").replace(",","+")
        query_string = query_string + "&mode=" + self.mode + "&sensor=false"
        web_obj =urllib.request.urlopen(query_string)
        results_str = str(web_obj.read())
        web_obj.close()
        return results_str
   
    def __lt__(self, other):
        if (self.distance() < other.distance()):
            return True 
        return False  
    def __gt__(self, other):
        if (self.distance() > other.distance()):
            return True 
        return False
    def __eq__(self, other):
        if (self.distance() == other.distance()):
            return True 
        return False    
    def __add__(self, other):
        my_cities = copy.deepcopy(self.cities)
        my_states = copy.deepcopy(self.states)
        other_cities = copy.deepcopy(other.cities)
        other_states = copy.deepcopy(other.states)
        my_cities = my_cities + other_cities
        my_states = my_states + other_states
        temp = Tour()
        temp.cities = my_cities
        temp.states = my_states
        return temp

    def __mul__(self, times):
        try:
            assert times >= 0
            temp = Tour()
            for i in range(times):
                temp = temp+self
            return temp
        except TypeError: 
            print("Negative value typeerror")
            
    
    
def main():
    
    t1 = Tour ( "New York , NY","Lansing, MI", "Kent,   OH")
    t2 = Tour ( "New York , NY","Lansing, MI", "Kent,   OH")
    print(t1==t2)

    t3 = Tour ( "New York , NY","Lansing, MI", "Kent,   OH")
    print(t3)
    t4 = Tour ( "New York , NY","Lansing, MI")
    print(t4)

    print(t3 < t4)
    print(t4 < t3)
    print(t3 > t4)
    print(t3 == t4)
    print(t3)
    print(t3.distance())

    print(t4)
    print(t4.distance())
    t5 = t3+t4 
    print(t5)
    print(t5.distance())
    
    t6 = Tour ( "New York , NY","Lansing, MI")
    print(t6)
    t7 = t6 * (5)
    print (t7)

    t8 = Tour ( "New York , NY","Lansing, MI")
    print(t6)
    t9 = t6 * (-5)
    print (t7)


if __name__== "__main__":
    main()