import binascii
import configparser
import logging.handlers
import os
import socket
import struct
import time
from datetime import time, datetime, timedelta
import pymysql.cursors

mydir = os.path.dirname(os.path.abspath(__file__))
config = configparser.RawConfigParser()
config.read([mydir + '/config-default.cfg', mydir + '/config.cfg'])
sql_host, sql_user, sql_pass, sql_db = config.get('mysql', 'mysql_host'), config.get('mysql', 'mysql_user'), \
                                       config.get('mysql', 'mysql_pass'), config.get('mysql', 'mysql_db')
HOST, PORT = config.get('server', 'ip'), config.getint('server', 'port')
SN = config.getint('WIFIKIT', 'sn')

LOG_FILE = 'log.txt'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)

fmt = '%(asctime)s -  %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('tst')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def packshort(data):
    if data == -1 or data == -10 or data == -100:  # The omnik uses 65535 as -1
        data = 65535
    return struct.pack('!H', data)


def packlong(data):
    return struct.pack('!I', data)


def packsn(data):
    return struct.pack('L', data)


def datasend():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((HOST, PORT))
    except Exception as e:
        print(e)
        logger.debug(e)
    else:
        try:
            conn = pymysql.connect(sql_host, sql_user, sql_pass, sql_db)
        except Exception as e:
            logger.debug(e)
            print(e)
        else:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            with conn:
                cursor.execute("SELECT * FROM minutes where ServerStamp > NOW() -  INTERVAL 5 MINUTE ")
                rows = cursor.fetchall()
            numrows = int(cursor.rowcount)
            conn.commit()
            cursor.close()
            conn.close()
            if numrows == 0:
                print("无数据上传")
            else:
                for i in range(0, numrows):
                    row = rows[i]
                    data = "688151B0"\
                           + str(binascii.b2a_hex(packsn(SN)))[2:-1] + str(binascii.b2a_hex(packsn(SN)))[ 2:-1] \
                           + "810201" \
                           + str(binascii.b2a_hex(row['InvID'].encode("utf8")))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['Temp'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['VPV1'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['VPV2'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['VPV3'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['IPV1'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['IPV2'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['IPV3'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['IAC1'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['IAC2'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['IAC3'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['VAC1'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['VAC2'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['VAC3'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(int(row['FAC'] * 100))))[2:-1] \
                           + str(binascii.b2a_hex(packshort(row['PAC1'])))[2:-1] \
                           + str(binascii.b2a_hex(packshort(row['PAC2'])))[2:-1] \
                           + str(binascii.b2a_hex(packshort(row['PAC3'])))[2:-1] \
                           + "FFFFFFFF" \
                           + str(binascii.b2a_hex(packshort(int(row['EToday'] * 100))))[2:-1] \
                           + str(binascii.b2a_hex(packlong(int(row['ETotal'] * 10))))[2:-1] \
                           + str(binascii.b2a_hex(packlong(row['HTotal'])))[2:-1] \
                           + "00010000000000000000000000000000000000000000000000000000000000000000000" \
                             "00000000000000000000000000000000000000000000000000000"
                    ver = 0
                    result = []
                    for n in range(int(len(data) / 2)):
                        j = n * 2 + 2
                        re = data[n * 2:j]
                        re1 = hex(eval('0x' + re))
                        ver = ver + eval(re1)
                        result.append(re)
                    senddata = "".join(result) + hex((ver - 104) & 0xff)[2:] + "16"
                    print(i, senddata)
                    logger.info(senddata)
                    sk.sendall(binascii.a2b_hex(senddata))
                    time.sleep(1)
    finally:
        sk.close()


if __name__ == "__main__":
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    print(strnow)
    period = timedelta(days=0, hours=0, minutes=5, seconds=0)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print("第一次上传时间:", strnext_time)
    while True:
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            print(iter_now_time)
            datasend()
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print("下一次上传时间: %s" % strnext_time)
            continue
