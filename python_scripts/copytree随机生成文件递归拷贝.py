#!/usr/bin/env python
# 要求：
# 1.选择一个已存在目录，其下创建 a/b/c/d 子目录解构，每个子目录下随机生成50个普通文件，文件名随机4个小写字母构成
# 2.将 a 目录所有内容拷贝到 dst 目录下，拷贝的普通文件名开头必须是 x,y,z 的

from pathlib import Path
import string, random, re, shutil
ALPHABET = string.ascii_lowercase

def filename(n):
    return "".join(random.choices(ALPHABET, k=n))

def exist_dir(dir):
    if not dir.exists():
        dir.mkdir()
    return dir

def file_manager(n=20):
    current_dir = exist_dir(Path('tmp'))
    exist_dir(current_dir / ('a/b/c/d'))
    src_dir = exist_dir(current_dir / 'a')
    dst_dir = exist_dir(current_dir / 'dst')

    def _to_touch(dir):
        for file in dir.iterdir():
            if file.is_dir() and file != dst_dir and len(list(file.glob('*'))) < n:
                for i in range(n):
                    (file / filename(4)).touch()
                # 递归创建
                _to_touch(file)

    _to_touch(current_dir)

    def _filter_file(func, names):
        '过滤函数，返回以 非 x,y,z 开头的文件集合'
        return set(filter(lambda x: not re.search(r'^[xyz]', x), names))

    def _to_copy(src, dst):
        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=_filter_file)
        for file in src.iterdir():
            # 如果 src 下还有目录，递归拷贝（过滤）
            if file.is_dir():
                _to_copy(file, dst / (file.name))

    _to_copy(src_dir, dst_dir)

    def _del_file(dir):
        '仅删除指定目录下的为字母文件'
        # print(*[ path for path in (Path('tmp').rglob('**/[a-z]*')) if not path.is_dir() ], sep='\n')
        fs = [path for path in dir.rglob('**/[a-z]*') if not path.is_dir()]
        for j in fs:
            j.unlink()
    # _del_file(dst_dir)

# file_manager()