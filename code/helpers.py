import pandas as pd
import csv


def export_bfs_to_csv(experiment_path, results):

    results = results.split(',')
    print(results)

    results.pop()
    print(results)


    # Split the list into two lists by alternating elements
    ids = results[::2]
    directions = results[1::2]

    # Output the results
    print("ids", ids)
    print("directions", directions)

    converted_ids = []
    for id in ids:
        converted_id = chr(int(id))
        converted_ids.append(converted_id)

    print(converted_ids)
    
    df = pd.DataFrame()
    df['car'] = converted_ids
    df['move'] = directions
    print(df)

    df.to_csv(experiment_path, sep=',', columns=['car', 'move'], index=False)
    
    
    # new_ids = [ids[0]]
    # for i in range(1, len(ids)):
    #     if ids[i] != ids[i - 1]:
    #         new_ids.append(ids[i])
            

    
        
    # print(new_ids)
    # print(directions)

    
        

    # with open(experiment_path, 'w') as output_file:
    #     csv_writer = csv_writer(output_file)
    #     csv_writer.writerw(results)