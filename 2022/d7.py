from aocd import get_data


class Dir:
    def __init__(self, dirname, prevdir) -> None:
        self.dirname = dirname
        self.prevdir = prevdir
        self.dirs = {}
        self.files = []
    
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f'Dir<dir={self.dirs}, files={self.files}>'
    
    def total_size(self):
        dirsize = sum(subdir.total_size() for subdir in self.dirs.values())
        return sum(fsize for _, fsize in self.files) + dirsize
    
    def all_dir_sizes(self):
        subdirs = [subdir.total_size() for subdir in self.dirs.values()]
        for subsub in self.dirs.values():
            subdirs.extend(subsub.all_dir_sizes())
        # for root dir, add its size as well
        if self.prevdir is None:
            subdirs.append(self.total_size())
        return subdirs
    
    def add_dir(self, dirname, dirptr):
        self.dirs[dirname] = dirptr
    def add_file(self, filename, size):
        self.files.append((filename, size))
    
    def get_prevdir(self):
        assert self.prevdir is not None
        return self.prevdir

    def get_dir(self, dirname):
        assert self.has_dir(dirname)
        return self.dirs[dirname]
    
    def has_dir(self, dirname):
        return dirname in self.dirs


def maybe_mkdir(curdir, dirname):
    if not curdir.has_dir(dirname):
        dirptr = Dir(dirname, curdir)
        curdir.add_dir(dirname, dirptr)
    return curdir.get_dir(dirname)


def parse_ls_output(fs, curdir, data, idx):
    topdir = curdir
    while idx < len(data):
        line = data[idx]
        if line.startswith('$'): break
        # read cmd output
        if line.startswith('dir'):
            _, dirname = line.split()
            curdir = maybe_mkdir(curdir, dirname)
        else:
            size, fname = line.split()
            curdir.add_file(fname, int(size))
        curdir = topdir
        idx += 1

    return idx


def build_hier(data):
    fs = Dir('/', prevdir=None)
    curdir = fs
    idx = 0

    while idx < len(data):
        line = data[idx]
        assert line.startswith('$')
        _, cmd = line.split('$')
        cmd = cmd.strip()
        if cmd.startswith('cd'):
            _, dirname = cmd.split()
            if dirname == '/':
                curdir = fs
            elif dirname == '..':
                curdir = curdir.get_prevdir()
            else:
                curdir = maybe_mkdir(curdir, dirname)
            idx += 1
        else:
            idx = parse_ls_output(fs, curdir, data, idx + 1)
    
    return fs


if __name__ == '__main__':
    data = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''
    data = get_data(year=2022, day=7)
    fs = build_hier(data.splitlines())
    #print(fs)
    #print(fs.total_size())
    all_dirs = fs.all_dir_sizes()

    # part 1
    print(sum(filter(lambda x: x <= 100000, all_dirs)))

    # part 2
    fs_size = 70000000
    update_size = 30000000
    current_free = fs_size - max(all_dirs)
    to_free_for_update = update_size - current_free
    candidate_dirs = filter(lambda x: x >= to_free_for_update, all_dirs)

    print(min(candidate_dirs))
