#! /usr/bin/env python

import datetime
import time
import signal
import sys
import sqlite3

conn = sqlite3.connect('money_manager.db')

def initDB():
    c = conn.cursor()
    c.execute("create table if not exists Transact (value FLOAT, currency TEXT, date INT, info TEXT)")
    conn.commit()
    c.close()


def addTransaction(date, total, currency, info):
    cur = conn.cursor()
    cur.execute("insert into Transact VALUES (?, ?, ?, ?)", (total, currency, time.mktime(date.timetuple()), info))
    conn.commit()
    cur.close()


def display():
    cur = conn.cursor()
    list = []
    total = 0
    for row in cur.execute('SELECT value, currency, date, info FROM Transact ORDER BY date'):
        list.append(row[2])
        total += row[0];
        print datetime.datetime.fromtimestamp(int(row[2])).strftime('%d/%m/%Y'), ", value: ", str(
            row[0])
    cur.close()
    print "total: ", total


if __name__ == "__main__":
    initDB()
    if len(sys.argv) < 2:
        print "add|display"
        sys.exit(0)
    elif (sys.argv[1] == "add"):
        print "Date of the transaction (dd/mm/yyyy): "
        datestring = sys.stdin.readline()
        print "Total: "
        total = sys.stdin.readline()
        print "Curency (euro?): "
        currency = sys.stdin.readline()
        if (currency.strip() == ""):
            currency = "euro"
        print "Info: "
        info = sys.stdin.readline()

        date = datetime.datetime.strptime(datestring.rstrip('\n'), '%d/%m/%Y')
        total = total.rstrip('\n')
        currency = currency.rstrip('\n')
        info = info.rstrip('\n')

        addTransaction(date, total, currency, info);
    elif (sys.argv[1] == "display"):
        display()
        sys.exit(0)
    else:
        print "add|display"
        sys.exit(0)

def signal_handler(signal, frame):
    sys.exit(0)