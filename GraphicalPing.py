import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ping
import datetime

#================================================================================
#
#================================================================================

#================================================================================
#   CONSTANTS
#================================================================================


#================================================================================
#   Globals
#       These are needed because callback functions are used.
#       Need to retain state across calls
#================================================================================
class MyGlobals:
    axis_pings = None
    ping_x_array = []
    ping_y_array = []
    ani = None
    fig = None

g_my_globals = MyGlobals()

class SpeedTestData:
    date_stamp = ''
    time_stamp = ''
    ping_time = 0.0
    download_speed = 0.0
    upload_speed = 0.0

#================================================================================
#   Function:   TAIL        Helper function
#       Reads the last N lines from a file
#================================================================================
def tail(f, n):
    assert n >= 0
    pos, lines = n+1, []
    while len(lines) <= n:
        try:
            f.seek(-pos, 2)
        except IOError:
            f.seek(0)
            break
        finally:
            lines = list(f)
        pos *= 2
    return lines[-n:]

#================================================================================
#   Function:   ANIMATE_PING
#       Call-back function
#       Called for every graph update
#       Performs *** PING! ***
#================================================================================
def animate_ping(j):
    global g_my_globals                 # graphs are global so that can be retained across multiple calls to this callback

        #===================== Do the ping =====================#
    response = ping.quiet_ping('google.com',timeout=300)
    if response[0] == 0:
        ping_time = 1000
    else:
        ping_time = response[0]
    #===================== Store current ping in historical array =====================#
    g_my_globals.ping_x_array.append(len(g_my_globals.ping_x_array))
    g_my_globals.ping_y_array.append(ping_time)
    # ===================== Only graph last 100 items =====================#
    if len(g_my_globals.ping_x_array) > 100:
        x_array = g_my_globals.ping_x_array[-100:]
        y_array = g_my_globals.ping_y_array[-100:]
    else:
        x_array = g_my_globals.ping_x_array
        y_array = g_my_globals.ping_y_array

    # ===================== Call graphinc functions =====================#
    g_my_globals.axis_ping.clear()                                                              # clear before graphing
    set_chart_labels()                                                                          # draw the labels
    g_my_globals.axis_ping.plot(x_array,y_array)                                                # graph the ping values

#================================================================================
#   Function:   Set graph titles and Axis labels
#       Sets the text for the subplots
#       Have to do this in 2 places... initially when creating and when updating
#       So, putting into a function so don't have to duplicate code
#================================================================================
def set_chart_labels():
    global g_my_globals

    g_my_globals.axis_ping.set_xlabel('Time')
    g_my_globals.axis_ping.set_ylabel('Ping (ms)')
    g_my_globals.axis_ping.set_title('Current Ping Duration', fontsize = 12)

#================================================================================
#   Function:   MAIN
#================================================================================
def main():
    global g_my_globals

    fig = plt.figure()
    g_my_globals.fig = fig

    g_my_globals.axis_ping = fig.add_subplot(1,1,1)

    set_chart_labels()
    plt.tight_layout()

    g_my_globals.ani_ping = animation.FuncAnimation(fig, animate_ping, interval=1000)
    plt.show()

if __name__ == '__main__':
    main()
