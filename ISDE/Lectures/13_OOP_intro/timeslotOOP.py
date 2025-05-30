class Timeslot:
    _minutes_in_hours = 60

    def __init__(self, hours = 0, minutes = 0):
        self._hours = int(hours + (minutes / Timeslot._minutes_in_hours))
        self._minutes = int(minutes % Timeslot._minutes_in_hours)

    @property
    def hours(self):
        return self._hours

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self,minutes):
        if minutes >= 60:
            print("minute value >= 60!")
        else:
            self._minutes = int(minutes)

    @hours.setter
    def hours(self,hours):
        self._hours = int(hours)

    def __repr__(self):
        return f"SONO LE ORE = {self._hours}:{self._minutes}"

    #create a new timeslot by summing two timeslots
    def __add__(self, other):
        minutes = self.minutes + other.minutes%self._minutes_in_hours
        hours = self.hours + other.hours + other.minutes/self._minutes_in_hours

        new_timeslot = Timeslot()
        new_timeslot.hours = hours
        new_timeslot.minutes = minutes
        return new_timeslot



