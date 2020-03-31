import ujson
import time
import _thread

from display import showState
import uwebsockets.client

THREAD_ALIVE = 0
THREAD_KILL = 1
THREAD_DEAD = 2

curstate = {}

def show():
    perc = 0
    if curstate.get('elapsed') > 0 and curstate.get('duration') > 0:
      perc = (curstate.get('elapsed') / curstate.get('duration')) * 100
    showState(curstate.get('state'), curstate.get('title'), curstate.get('artist'), perc)

def start_progress():
    global thread_state
    while curstate.get('elapsed') < curstate.get('duration'):
        #update progress
        curstate['elapsed'] = curstate.get('elapsed') + 1
        show()
        #wait for one second
        time.sleep(1)
        #check to see if the thread is being killed
        if thread_state == THREAD_KILL:
            #thread being killed, show we're killing it
            thread_state = THREAD_DEAD
            #exiting
            _thread.exit()

def main():
    websocket = uwebsockets.client.connect('ws://192.168.68.124:3000')
    mesg = '{ "event": "getStatus", "data": {} }'
    websocket.send(mesg + "\r\n")
    lock = _thread.allocate_lock()
    global thread_state
    while True:
        json = websocket.recv()
        resp = ujson.loads(json)
        data = resp['data']
        if resp.get('event') == 'pushStatus':
            #stop any progress updates
            if thread_state == THREAD_ALIVE:
                #acquire lock
                lock.acquire()
                #set kill message
                thread_state = THREAD_KILL
                #wait for death
                while thread_state != THREAD_DEAD:
                    #waiting
                    pass
                #thread dead, release thread
                lock.release()

            #set data
            curstate['state'] = data.get('state')
            curstate['title'] = data.get('title', 'stopped')
            curstate['artist'] = data.get('artist', '')
            curstate['elapsed'] = data.get('elapsed', 0)
            curstate['duration'] = data.get('duration', 0)

            #if we're playing, start the progress thread
            if curstate.get('state') == 'play':
                #time to play
                thread_state = THREAD_ALIVE
                _thread.start_new_thread(start_progress, ())
            else:
                #we're not playing, so just put up the status once
                show()

thread_state = THREAD_DEAD
_thread.start_new_thread(main, ())
