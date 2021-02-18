class Clock:

    def __init__(self, h=12, m=30, s=00):
        self.hours = h
        self.minutes = m
        self.seconds = s

    def __repr__(self):
        return f"{type(self).__name__}({self.hours:02d}, {self.minutes:02d}, {self.seconds:02d})"

    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    def __add__(self, other):
        s = (self.seconds + other.seconds) % 60
        m = ((self.minutes + other.minutes) + (self.seconds + other.seconds) // 60) % 60
        h = ((self.hours + other.hours) + (self.minutes + other.minutes) // 60) % 24
        return Clock(h, m, s)

    def str_update(self, clock_string):
        if ":" in clock_string:
            split = clock_string.split(":")
            if len(split) == 3:
                try:
                    h = int(split[0])
                    m = int(split[1])
                    s = int(split[2])
                except:
                    raise ValueError("Format must be hh:mm:ss")
                if h < 24 and m < 60 and s < 60:
                    self.hours = h
                    self.minutes = m
                    self.seconds = s
                    return

        raise ValueError("Format must be hh:mm:ss")


if __name__ == "__main__":
    # init
    c = Clock(22, 30, 30)
    d = Clock(1, 30, 30)

    # str_update
    c.str_update("14:57:45")

    # print_clock
    print(c)
    print(d)

    # add clocks
    print("Adding the two clocks above")
    print(c + d)



