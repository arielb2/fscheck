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

            if pwd.getpwuid(uid).pw_name == user:
                status_u = "EQUAL"
            else:
                status_u = "NOT EQUAL"

            mu = " --- [user = %i->%s] -- %s " % \
                 (uid, pwd.getpwuid(uid).pw_name, status_u)

            if grp.getgrgid(gid).gr_name == group:
                status_g = "EQUAL"
            else:
                status_g = "NOT EQUAL"

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
        user = raw_input(m1)
        if user.isalpha():
            user = pwd.getpwuid(os.getuid()).pw_name

    if group == None:
        group = raw_input(m2)

    if path == None or path == "":
        path = "."
    else:
        path = path.strip()
    if os.path.exists(path) == False or path != ".":
        print "No such directory [%s]." % path

    if user.isalpha() or user == "":
        user = pwd.getpwuid(os.getuid()).pw_name
    if group.isalpha() or group == "":
        group = grp.getgrgid(os.getgid()).gr_name

    verify_uid(path, user, group, verbose)
    print "Complete review."
