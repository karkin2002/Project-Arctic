
import data.scripts.globalVar as globalVar
globalVar.init()

import data.scripts.ThreadingVar as threadVar
threadVar.init()

import time




def checkChunkQueue(game):
    """Checks, processes and deletes chunk items in a queue. This functon
    should be threaded
    """    

    map_extra_chunk_queue = []

    try:
        while globalVar.run:
            time.sleep(game.CHUNK_QUEUE_TIME)

            if game.map_name != None:

                    threadVar.checking_queue = True

                    for chunk in threadVar.map_chunk_queue:
                        
                        ## Checks if a chunk in the queue is waiting, if it
                        ## is it creates a map chunk surface and labes it as
                        ## "done"

                        if threadVar.map_chunk_queue[chunk][0] == "Waiting":
                            threadVar.map_chunk_queue[chunk][0] = "Processing"
                            chunk_info = chunk.split(",")
                            map_extra_chunk_queue = game.getMap(game.map_name).createMapChunkSurface( chunk_info[0], (int(chunk_info[1]), int(chunk_info[2])))


                    ## Adds extra edge chnks to queue if they need be
                    for extra_chunk in map_extra_chunk_queue:
                        threadVar.map_chunk_queue[extra_chunk] = map_extra_chunk_queue[extra_chunk]

                    ## Deletes any chunks with label done
                    for chunk in threadVar.delete_chunk_queue:
                        del threadVar.map_chunk_queue[chunk]

                    threadVar.delete_chunk_queue = {}

                    threadVar.checking_queue = False
            
    except Exception as e: print(e)
            


def requestChunk(map_chunks: dict, map_layer: str, x: int, y: int):
    
    """Checks if the chunk has been loaded, and if it hasn't adds it to a queue
    to be loaded.
    """    

    if not threadVar.checking_queue:
        if map_chunks[map_layer][f"{x},{y}"] == None:
            
            chunk_key = f"{map_layer},{x},{y}"
            
            if chunk_key not in threadVar.map_chunk_queue:
                threadVar.map_chunk_queue[chunk_key] = ["Waiting", None]
