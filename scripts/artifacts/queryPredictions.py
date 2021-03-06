import glob
import os
import pathlib
import plistlib
import sqlite3
import scripts.artifacts.artGlobals #use to get iOS version -> iOSversion = scripts.artifacts.artGlobals.versionf

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, is_platform_windows 
from scripts.ccl import ccl_bplist

def get_queryPredictions(files_found, report_folder, seeker):
    file_found = str(files_found[0])
    db = sqlite3.connect(file_found)
    cursor = db.cursor()
    cursor.execute('''
    select
    datetime(creationTimestamp, "UNIXEPOCH") as START, 
    content,
    isSent,
    conversationId,
    id,
    uuid
    from messages 
    ''')
    all_rows = cursor.fetchall()
    usageentries = len(all_rows)
    if usageentries > 0:
        data_list = []
        for row in all_rows:    
            data_list.append((row[0],row[1],row[2],row[3],row[4],row[5]))

        report = ArtifactHtmlReport('Query Predictions')
        report.start_artifact_report(report_folder, 'Query Predictions')
        report.add_script()
        data_headers = ('Timestamp','Content','Is Sent?','Conversation ID','ID','UUID')   
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()
        
        tsvname = 'Query Predictions'
        tsv(report_folder, data_headers, data_list, tsvname)
    else:
        logfunc('No data available in table')

    db.close()
    return   