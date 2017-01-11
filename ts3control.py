"""
Manage a teamspeak 3 query instance from your CLI.
"""

import argparse
import ts3
from ts3.defines import *
import sys
import time
from prettytable import PrettyTable

def main():
    parser = argparse.ArgumentParser(description=__doc__)

    subparsers = parser.add_subparsers(help='commands')

    # A list command
    list_parser = subparsers.add_parser('list', help='List all servers')
    list_parser.add_argument('-s','--status', default='all', action='store', help='Declare server status to display', type=str)

    # A create command
    create_parser = subparsers.add_parser('create', help='Create a new server')
    create_parser.add_argument('-n','--name', action='store', help='New server name as string.', type=str, dest='new_name')
    create_parser.add_argument('-p','--port', action='store', help='New server port', type=int, dest='new_port')
    create_parser.add_argument('-s','--slots', default=5, action='store',help='Number of server slots.', dest='new_slots')

    # A delete command
    delete_parser = subparsers.add_parser('delete', help='Remove a server')
    delete_parser.add_argument('-id','--id', action='store', help='The server ID to remove', dest='server_id')

    # A server token creator command
    list_parser = subparsers.add_parser('token', help='Create a server group token.')
    list_parser.add_argument('-id','--virtualid', action='store', help='Select server.', type=int)
    list_parser.add_argument('-sg','--servergroup', action='store', help='Select server group to create a token for.', type=str)

    # A start command
    delete_parser = subparsers.add_parser('start', help='Start a server')
    delete_parser.add_argument('-id','--id', action='store', help='The server ID to start', dest='start_id')

    # A stop command
    delete_parser = subparsers.add_parser('stop', help='Stop a server')
    delete_parser.add_argument('-id','--id', action='store', help='The server ID to remove', dest='stop_id')

    # A restart command
    delete_parser = subparsers.add_parser('restart', help='Restart a server')
    delete_parser.add_argument('-id','--id', action='store', help='The server ID to remove', dest='restart_id')

    # A Global message command
    delete_parser = subparsers.add_parser('gm', help='Send a message to all servers')
    delete_parser.add_argument('-m','--message', action='store', help='The broadcasting message', dest='msg', type=str, required=True)

    args = vars(parser.parse_args())

    ########################################################

    try:
        conn = ts3.TS3Server('triscle.de', 10011)
        conn.login('serveradmin', 'eVsZO6LZ')
    except:
        print 'Connection error.'
    else:
        servers = conn.send_command('serverlist').data

    # list servers
    if 'status' in args:
        t = PrettyTable(['ID', 'Name', 'Port', 'Status', 'Clients'])
        t.align = 'l'
        t.align['Name'] = 'c'
        if args['status'] == 'all':
            for server in servers:
                uid = server['virtualserver_id']
                name = server['virtualserver_name']
                port = server['virtualserver_port']
                status = server['virtualserver_status']
                try:
                    clients = server['virtualserver_clientsonline'].encode('utf-8')
                    max_clients = server['virtualserver_maxclients'].encode('utf-8')
                except:
                    clients = 0
                    max_clients = 0
                user_status = "{curr}/{max}".format(curr=clients, max=max_clients)
                t.add_row([uid, name, port, status, user_status])
            print t
        elif args['status'] == 'online':
            for server in servers:
                status = server['virtualserver_status']
                if status == 'online':
                    uid = server['virtualserver_id']
                    name = server['virtualserver_name']
                    port = server['virtualserver_port']
                    clients = server['virtualserver_clientsonline'].encode('utf-8')
                    max_clients = server['virtualserver_maxclients'].encode('utf-8')
                    user_status = "{curr}/{max}".format(curr=clients, max=max_clients)
                    t.add_row([uid, name, port, status, user_status])
            print t
        elif args['status'] == 'offline':
            for server in servers:
                status = server['virtualserver_status']
                if status == 'offline':
                    uid = server['virtualserver_id']
                    name = server['virtualserver_name']
                    port = server['virtualserver_port']
                    clients = 0
                    max_clients = 0
                    user_status = "{curr}/{max}".format(curr=clients, max=max_clients)
                    t.add_row([uid, name, port, status, user_status])
            print t
        else:
            print 'Usage: list -s online/offline/all'


    # Create Server
    try:
        info = [args['new_name'], args['new_port'], args['new_slots']]
    except:
        pass
    else:
        if all(info):
            t = PrettyTable(['Name', 'Port', 'Slots'])
            t.add_row(info)
            print '\nCreating New Server with following information:'
            print t, "\n"
            confirm = raw_input('Are you sure you want to create this server? (y/n): ')
            if 'y' in confirm.lower():
                response = conn.send_command("servercreate virtualserver_name='{}' virtualserver_port={} virtualserver_maxclients={}".format(args['new_name'], args['new_port'], args['new_slots']))
                if response.is_successful:
                    print 'Server created successfully!'
                    print 'Server ID: {}'.format(response.data[0]['sid'])
                else:
                    sys.exit("Error creating server: %s" % response.response['msg'])
        else:
            print "Usage: create -n 'NAME' -p PORT -s SLOTS"

    # delete server
    if 'server_id' in args:
        if args['server_id'] == None:
            print "Usage: delete -id SERVERID"
        else:
            t = PrettyTable(['ID', 'Name', 'Port', 'Status', 'Clients'])
            t.align = 'l'
            t.align['Name'] = 'c'
            for server in servers:
                if server['virtualserver_id'] == args['server_id']:
                    uid = server['virtualserver_id']
                    name = server['virtualserver_name']
                    port = server['virtualserver_port']
                    status = server['virtualserver_status']
                    clients = server['virtualserver_clientsonline'].encode('utf-8')
                    max_clients = server['virtualserver_maxclients'].encode('utf-8')
                    user_status = "{curr}/{max}".format(curr=clients, max=max_clients)
                    t.add_row([uid, name, port, status, user_status])
            print t
            choice = raw_input('Do you really want to delete this server? (y/n): ')
            if 'y' in choice.lower():
                if status == 'online':
                    conn.send_command('serverstop sid={}'.format(args['server_id']))
                response = conn.send_command("serverdelete sid={}".format(args['server_id']))
                if response.is_successful:
                    print "Server {} deleted successfully.".format(args['server_id'])
                else:
                    sys.exit("Error deleting server: %s" % response.response['msg'])


    # server token creator
    if 'servergroup' in args:
        conn.use(args['virtualid'])
        servergroups = conn.send_command('servergrouplist').data
        for group in servergroups:
            if group['name'] == args['servergroup']:
                if group['sgid'] > 2:
                    group_id = group['sgid']
        response = conn.send_command("tokenadd tokentype=0 tokenid1={} tokenid2=0 tokendescription=CreatedByAdmin".format(group_id))
        if response.is_successful:
            print(response.data[0]['token'])
            sys.exit(0)
        else:
            sys.exit("Error creating key: %s" % response.response['msg'])

   # start a server
    if 'start_id' in args:
        for server in servers:
            if server['virtualserver_id'] == args['start_id']:
                if server['virtualserver_status'] == 'offline':
                    response = conn.send_command('serverstart sid={}'.format(args['start_id']))
                    if response.is_successful:
                        print "Server successfully started."
                else:
                    print 'Server is currently running.'

    # stop a server
    if 'stop_id' in args:
        for server in servers:
            if server['virtualserver_id'] == args['stop_id']:
                if server['virtualserver_status'] == 'online':
                    response = conn.send_command('serverstop sid={}'.format(args['stop_id']))
                    if response.is_successful:
                        print "Server successfully stopped."
                else:
                    print 'Server is currently not running.'

    # restart a server
    if 'restart_id' in args:
        for server in servers:
            if server['virtualserver_id'] == args['restart_id']:
                if server['virtualserver_status'] == 'online':
                    response = conn.send_command('serverstop sid={}'.format(args['restart_id']))
                    if response.is_successful:
                        print "Server stopped."
                        time.sleep(1)
                        print "Restarting..."
                        time.sleep(2)
                        response = conn.send_command('serverstart sid={}'.format(args['restart_id']))
                        if response.is_successful:
                            print "Server restarted successfully."
                else:
                    print "Server already stopped."
                    print "Restarting..."
                    response = conn.send_command('serverstart sid={}'.format(args['restart_id']))
                    time.sleep(2)
                    if response.is_successful:
                        print "Server (re)started successfully."


    if 'msg' in args:
        response = conn.send_command('gm msg={}'.format(args['msg']))
        if response.is_successful:
            print "{} sent to all servers.".format(args['msg'])
        else:
            sys.exit("Error sending message: %s" % response.response['msg'])

    ########################################################

if __name__ == '__main__':
    main()
