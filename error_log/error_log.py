from time import localtime

def construct_log_entry( lt, err ):
    time      = "Time {} : {}".format( lt.tm_hour, lt.tm_min )
    date      = "Date {} - {} - {}".format(  lt.tm_mon, lt.tm_mday, lt.tm_year ) 
    border    = '*' * 100 + '\n'
    heading   = '\n'.join( ['\n', time, date, border] )
    tailing   = border
    log_entry = '\n'.join( [heading, err, tailing] )
    return log_entry

def append_log( err ):
    log_entry = construct_log_entry( localtime(), err )

    # Important caveat: make sure the program has the access rights to write to error_log/error_log.txt.
    with open( 'error_log/error_log.txt', 'a' ) as f:
        f.write( log_entry )
