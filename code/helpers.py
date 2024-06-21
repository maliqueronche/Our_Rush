import pandas as pd
import csv

def export_results_to_csv(export_path, results):
    '''Takes export path and results and writes results to csv.'''
    
    with open(export_path, 'w') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(results)


def export_bfs_to_csv(export_path, results):
    '''Takes export path and results and writes results to csv.'''

    # Split results by comma and remove last element if empty string
    results = results.split(',')
    if results[-1] == '':
        results.pop()
    
    # Split list into two lists by alternating elements
    ids = results[::2]
    moves = results[1::2]
    moves_caracter = []
    for move in moves:
        if move == '+':
            move = '1'
        elif move == '-':
            move = '-1'
        moves_caracter.append(move)

    # Convert ids from ord to chr
    converted_ids = []
    for id in ids:
        converted_id = chr(int(id))
        converted_ids.append(converted_id)

    # Create dataframe, add ids, moves and export to csv
    df = pd.DataFrame()
    df['car'] = converted_ids
    df['move'] = moves_caracter
    df.to_csv(export_path, sep=',', columns=['car', 'move'], index=False)