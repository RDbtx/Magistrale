#first implementation of a time_slot program through the use of dictionaries

minutes_in_hour = 60

def implementation01():
    #memory allocated to this implementation is doubled since i store hours and minutes
    def create_time_slot(h = 0, m=0):
        time_slot = {'hours': h, 'minutes': m}
        return time_slot

    def set_h_min(time_slot,h,m):
        time_slot['hours'] = h
        time_slot['minutes'] = m

    def set_min(time_slot,m):
        time_slot['hours'] = int(m/minutes_in_hour)
        time_slot['minutes'] = m% minutes_in_hour

    def get_h_min(time_slot):
        return time_slot['hours'],time_slot['minutes']

    def get_min(time_slot):
        return (time_slot['hours']* minutes_in_hour) + timeslot['minutes']



    timeslot = create_time_slot()
    set_h_min(timeslot,2,20)
    print(get_h_min(timeslot))
    print(get_min(timeslot))

    set_min(timeslot,250)
    print(get_h_min(timeslot))
    print(get_min(timeslot))

def implementation02():
    #halved the memory space cost since only it stores minutes and obtain the hours variable from them

    def create_timeslot(h= 0, m = 0):
        minutes = h * minutes_in_hour + m
        time_slot = {'minutes': minutes}
        return time_slot

    def set_h_min(time_slot,h,m):
        minutes = h * minutes_in_hour + m
        time_slot['minutes'] = minutes

    def set_min(time_slot,m):
        time_slot['minutes'] = m

    def get_min(time_slot):
        return int(time_slot['minutes'])

    def get_h_min(time_slot):
        hours = time_slot['minutes']/minutes_in_hour
        minutes = time_slot['minutes']%minutes_in_hour
        return int(hours),int(minutes)

    time = create_timeslot()
    set_min(time,250)
    print(f"\ntempo in minuti: {get_min(time)}")
    print(f"sono le ore: {get_h_min(time)[0]}:{get_h_min(time)[1]}")

    set_h_min(time,15,250)
    print(f"\ntempo in minuti: {get_min(time)}")
    print(f"sono le ore: {get_h_min(time)[0]}:{get_h_min(time)[1]}")


implementation02()