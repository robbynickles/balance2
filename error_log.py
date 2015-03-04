from time import localtime

def write_error_to_log( err ):
    with open( 'error_log', 'a' ) as f:
        lt        = localtime()
        time      = "Time {} : {}".format( lt.tm_hour, lt.tm_min )
        date      = "Date {} - {} - {}".format(  lt.tm_mon, lt.tm_mday, lt.tm_year ) 
        border    = '*' * 100 + '\n'
        heading   = '\n'.join( ['\n', time, date, border] )
        tailing   = border
        log_entry = '\n'.join( [heading, err, tailing] )

        f.write( log_entry )
