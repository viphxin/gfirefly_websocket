import gevent
if __name__ == "__main__":
    try:
        gevent.Timeout(0.1).start()
        gevent.sleep(0.2)
    except BaseException, e:
        print 'e'*20

