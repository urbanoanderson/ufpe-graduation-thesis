#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import time

class Timer(object):

    def __init__(self):
        self.stopped = True
        self.Reset()

    def Start(self):
        self.tstart = time.time()
        self.stopped = False

    def Stop(self):
        self.tend = time.time()
        self.stopped = True

    def Reset(self):
        self.tstart = time.time()
        self.tend = time.time()

    #Return elapsed time in secs (float)
    def Elapsed(self):
        if(not self.stopped):
            self.tend = time.time()
        return self.tend - self.tstart

#Usage
#if __name__ == '__main__':
    #timer = Timer()
    #timer.Start()
    #for i in range(100000000):
        #a = i
    #timer.Stop()
    #print timer.Elapsed(), ' secs'
