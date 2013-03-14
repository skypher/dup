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

        print("Finding dupes...")
        sys.stdout.flush()

        i = 0
        while i < nfiles:
            file = files[i]

            print("(%d/%d) %s" % (i+1, nfiles, file))

            dupes = []
            for j in range(i+1, nfiles-1):
              candidate = files[j]
              if candidate.size != file.size or candidate.hash() != file.hash():
                  break
              dupes.append(candidate)

            if dupes:
                print("\nDUPES FOUND:\n  SIZE: %s bytes  HASH: %s" % (file.size_str(), file.hash()))

                i += len(dupes)

                dupes.insert(0, file)

                k = 1
                for dupe in dupes:
                  print("  (%d) %s" % (k, dupe))
                  k += 1

                print()

                def select_dupes(dupes):
                    if len(dupes) <= 2:
                        sys.stdout.write('Delete which one (1/2, <Return> for none)? ')
                        sys.stdout.flush()

                        ch = getch()
                        print(ch)
                        sys.stdout.flush()

                        if (ord(ch) == 13):
                            return []

                        try:
                            ch = int(ch)
                        except ValueError:
                            return select_dupes(dupes)

                        if ch in [1,2]:
                            return [dupes[ch-1]]
                            return select_dupes(dupes)
                    else:
                        sys.stdout.write("Delete which ones (e.g. '2,3', <Return> for none)? ")
                        sys.stdout.flush()

                        selection = input().split(',')

                        if selection == ['']:
                            return []

                        result = []
                        for ch in selection:
                            try:
                                ch = int(ch)
                            except ValueError:
                                return select_dupes(dupes)
                            result.append(ch)

                        return [dupes[s-1] for s in result]


                for dupe in select_dupes(dupes):
                    os.remove(dupe.name)
                    print('Deleted file %s' % dupe.name)

                print()

            i += 1

    except BrokenPipeError:
        pass

