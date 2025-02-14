# © 2023 by InfinityNing. All rights reserved.
#
# data structure for sqlite db file:
# |  cid  |  name   |  type       |
# |   0   |  id     |  INTEGER    |
# |   1   |  title  |  CHAR(200)  |
# |   2   |  data   |  BLOB       |

import sqlite3
import os

query_id_sql = """
    SELECT id FROM main.content
"""
query_data_by_id_sql = """
    SELECT title, data FROM main.content WHERE id = {}
"""

cur_dir = os.path.dirname(__file__)
store_dir = "{}\\export".format(cur_dir)
db_file = "{}\\test.db".format(cur_dir)

def create_dir(dir):
    """
    create output dir
    """
    if not os.path.exists(dir):
        os.makedirs(dir)

def store_file(dir, title, blob_data):
    """
    for each blob_data, save as seperate file
    """
    file_path = ("{}\\{}.pdf" if is_pdf(blob_data) else "{}\\{}").format(dir, title)
    with open(file_path, "wb") as f:
        f.write(blob_data)
    print("\tstored: {}".format(file_path))

def is_pdf(blob_data):
    """
    judge if blob data matches pdf file format
    """
    if blob_data[4:8].hex() != "25504446":
        # print_head(blob_data=blob_data)
        return False
    return True

def print_head(blob_data):
    """
    print top 72 bytes of blob data
    """
    print(
        blob_data[:8].hex() + "\t" + 
        blob_data[8:16].hex() + "\t" + 
        blob_data[16:24].hex() + "\t" + 
        blob_data[24:32].hex() + "\t" + 
        blob_data[32:40].hex() + "\t" + 
        blob_data[40:48].hex() + "\t" + 
        blob_data[48:56].hex() + "\t" + 
        blob_data[56:64].hex() + "\t" + 
        blob_data[64:72].hex()
    )

def print_tail(blob_data):
    """
    print last 72 bytes of blob data
    """
    print(
        blob_data[-72:-64].hex() + "\t" + 
        blob_data[-64:-56].hex() + "\t" + 
        blob_data[-56:-48].hex() + "\t" + 
        blob_data[-48:-40].hex() + "\t" + 
        blob_data[-40:-32].hex() + "\t" + 
        blob_data[-32:-24].hex() + "\t" + 
        blob_data[-24:-16].hex() + "\t" + 
        blob_data[-16:-8].hex() + "\t" + 
        blob_data[-8:].hex()
    )

def process():
    """
    process all data stored in sqlite db as blob
    """
    if not os.path.exists(db_file):
        print("no file found")
        exit(1)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(query_id_sql)
    ids = cursor.fetchall()
    total = len(ids)
    if total == 0:
        print("no file to be processed")
        exit(0)
    create_dir(store_dir)
    for index, id in enumerate(ids):
        # query blob_data seperately, avoid taking too much memory
        print("processing: {}/{}".format(index + 1, total))
        cursor.execute(query_data_by_id_sql.format(id[0]))
        result = cursor.fetchone()
        title = result[0]
        blob_data = result[1]
        store_file(dir=store_dir, title=title, blob_data=blob_data)
    conn.close()

if __name__ == "__main__":
    print("current dir: {}".format(cur_dir))
    process()