## File containing global varaiables using in threading

def init():
    global map_chunk_queue, delete_chunk_queue, checking_queue
    
    map_chunk_queue = {}
    
    delete_chunk_queue = {}
    
    checking_queue = False
