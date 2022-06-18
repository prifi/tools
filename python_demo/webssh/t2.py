
# re regular expression
import re
s = '192.168.142.140, python  python,   22'

# 建议先编译
# 30分钟学会正则 w3cschool
# \s 任意一个空白字符，空格 \t \f \r \n \v
pattern = '(?P<host>[\d.]+)[,\s]+(?P<username>[a-zA-Z0-9_-]+)[,\s]+(?P<password>\w+)[,\s]+(?P<port>\d+)' # 字符的集合，元字符，表示1个字符
regex = re.compile(pattern)

m = regex.match(s)
if m:
    print(m[0]) # 0组，表示match
    print(m.groups())# 有效分组从1开始
    print(m.groupdict())

