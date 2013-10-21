#/usr/bin/python
import os
import grp
import pwd
import sys
import getopt


def verify_uid(path, user, group, verbose):
    print "Processing...."
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            path_down = os.path.join(root, name)
            uid = os.stat(path_down).st_uid
            gid = os.stat(path_down).st_gid

            try:
                if pwd.getpwuid(uid).pw_name == user:
                    status_u = "EQUAL"
                else:
                    status_u = "NOT EQUAL"
            except KeyError:
                print "Error: unknown uid ['%s']. ['%s']" % (uid, path_down)
                sys.exit(2)

            mu = " --- [user = %i->%s] -- %s " % \
                 (uid, pwd.getpwuid(uid).pw_name, status_u)
            try:
                if grp.getgrgid(gid).gr_name == group:
                    status_g = "EQUAL"
                else:
                    status_g = "NOT EQUAL"
            except KeyError:
                print "Error: unknown gid ['%s']. ['%s']" % (gid, path_down)
                sys.exit(2)

            mg = " --- [group = %i->%s] -- %s " % \
                 (gid, grp.getgrgid(gid).gr_name, status_g)


            if status_u == "NOT EQUAL":
                print path_down
                print(mu)
            if status_g == "NOT EQUAL":
                print path_down
                print(mg)
            if verbose == True:
                print("%s " % path_down)
                print(" --- %s ", mu)
                print(" --- %s ", mg)


if __name__ == '__main__':

    m1 = "Input user - Default[%s]" % pwd.getpwuid(os.getuid()).pw_name
    m2 = "Input group - Default[%s] " % grp.getgrgid(os.getgid()).gr_name
    user = None
    group = None
    path = None
    verbose = False

    try:
      opts, args = getopt.getopt(sys.argv[1:], "h:p:u:g:v")
    except getopt.GetoptError:
      print 'fscheck.py -p <path> -u <user> -g <group> -v <[verbose]>'
      sys.exit(2)

    for opt, arg in opts:
        if opt == "-p":
            path =  arg
        elif opt == "-u":
            user = arg
        elif opt == "-g":
            group = arg
        elif opt == "-v":
            verbose = True
        elif opt == "-h":
           print 'fscheck.py -p <path> -u <user> -g <group> -v <[verbose]>'
           sys.exit(2)
    if path == None:
        path = raw_input("Input path - Default[.] ")

    if user == None:
        error = 1
        while(error):
            user = raw_input(m1)
            if user.isalpha() or user == "":
                user = pwd.getpwuid(os.getuid()).pw_name
                error = 0
            else:
                try:
                    pwd.getpwnam(user)
                    error = 0
                except KeyError:
                    print "Error: unknown user ['%s']" % user

    if group == None:
        error = 1
        while(error):
            group = raw_input(m2)
            if group.isalpha() or group == "":
                group = grp.getgrgid(os.getgid()).gr_name
                error = 0
            else:
                try:
                    grp.getgrnam(group)
                    error = 0
                except KeyError:
                     print "Error: unknown group ['%s']" % group

    if path == None or path == "":
        path = "."
    else:

        path = path.strip()
    if os.path.exists(path) == False and path != ".":
        print "No such directory [%s]." % path
        sys.exit(2)

    #if user.isalpha() or user == "":
    #    user = pwd.getpwuid(os.getuid()).pw_name
    #if group.isalpha() or group == "":
    #    group = grp.getgrgid(os.getgid()).gr_name

    #try:
    #    pwd.getpwnam(user)
    #except KeyError:
    #    print "Error: unknown user ['%s']" % user
    #    sys.exit(2)

    #try:
    #    pwd.getpwnam(group)
    #except KeyError:
    #    print "Error: unknown group ['%s']" % user
    #    sys.exit(2)

    verify_uid(path, user, group, verbose)
    print "Complete review."
