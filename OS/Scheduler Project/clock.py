class Clock :
    INTERVAL = .1
    # First thing in scheduler is to increment time
    __clk = -INTERVAL
    def __init__(self) : pass
    # Only scheduler can call this function
    def incTime(self) : Clock.__clk += Clock.INTERVAL
    def getTime(self) : return Clock.__clk
    def repTime(self) :
        t = Clock.__clk
        tmp = '%3.3f:' % t
        return tmp.zfill(8)
