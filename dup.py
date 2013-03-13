#!/usr/bin/python3
import os
import sys
import locale
import hashlib
import tty
import termios

class File:
    def __init__(self, name):
        self.name = name
        self.size = os.stat(name).st_size

    def __str__(self):
        return "%s (%s bytes)" % (self.name, self.size_str())

    def size_str(self):
        return locale.format("%d", self.size, grouping=True)

    __hash = None

    def hash(self):
        if (self.__hash is None):
            print('Calculating hash: %s' % self)
            sys.stdout.flush()
            md5 = hashlib.md5()
            file = open(self.name, mode='br')
            chunksize = 1024**2
            bytes_read = 0

            while True:
                chunk = file.read(chunksize)
                md5.update(chunk)
                sys.stdout.write('.')
                sys.stdout.flush()
                bytes_read += chunksize
                if bytes_read >= 10*chunksize:
                    break
                if len(chunk) < chunksize:
                    break
            print()

            self.__hash = md5.hexdigest()

        return self.__hash

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')

    try:
        if (len(sys.argv) < 2):
            print("Please pass file list filename as first arg.")
            sys.exit(1)

        files = []
        print("Reading files...")
        sys.stdout.flush()
        with open(sys.argv[1], mode='br') as f:
            for filename in f.readlines():
                filename = filename[:-1]
                try:
                    files.append(File(filename))
                except FileNotFoundError:
                    print("Warning: file not found: %s" % filename, file=sys.stderr)

        print("Sorting files by size...")
        sys.stdout.flush()
        files = sorted(files, key=lambda file: file.size, reverse=True)

        nfiles = len(files)
        lastfile = None
        i = 0
        print("Finding dupes...")
        sys.stdout.flush()
        for file in files:
            if (lastfile and file.size == lastfile.size and
                file.hash() == lastfile.hash()):
                print("\nDUPES FOUND:\n  SIZE: %s bytes  HASH: %s\n  (1) %s\n  (2) %s\n" %
                      (file.size_str(), file.hash(), file.name, lastfile.name))
                sys.stdout.write('Delete which one (1/2)? ')
                sys.stdout.flush()

                ch = getch()

                print(ch)
                if ch == '1':
                    os.remove(file.name)
                    print('Deleted file %s' % file.name)
                if ch == '2':
                    os.remove(lastfile.name)
                    print('Deleted file %s' % lastfile.name)
                else:
                    print()

            lastfile = file
            i += 1
            print("(%d/%d) %s" % (i, nfiles, file))
    except BrokenPipeError:
        pass

