from time import localtime

def write_error_to_log( err ):
    with open( 'error_log', 'a' ) as f:
        lt        = localtime()
        timestamp = "{} : {}     {} - {} - {}".format( lt.tm_hour, lt.tm_min, lt.tm_mon, lt.tm_mday, lt.tm_year ) 
        heading   = '\n' + timestamp + '\n' + '*' * 100 + '\n'
        tailing   = '\n' + '*' * 100 + '\n'

        f.write( heading )
        f.write( err )
        f.write( tailing )
