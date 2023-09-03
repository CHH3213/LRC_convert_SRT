import os
import sys
import re

if '--help' or '-h' in sys.argv:
  print("""Usage: 
  python lrc2srt.py -f <lrc_file> [-o <output_dir>]

  -f <lrc_file>   指定输入的lrc文件
  -o <output_dir> 指定输出srt文件的目录,可选
  --help          打印此帮助信息
  
  输出的srt文件名称将与输入lrc文件名一致
  """)
  exit(0)

lrc_file = None
srt_dir = None

for i in range(len(sys.argv)):
  if sys.argv[i] == '-f':
    lrc_file = sys.argv[i+1]  
  elif sys.argv[i] == '-o':
    srt_dir = sys.argv[i+1]

if lrc_file is None:
  print('Usage: python lrc2srt.py -f <lrc_file> [-o <output_dir>]')
  exit(1)

lrc_name = os.path.basename(lrc_file)  
srt_name = os.path.splitext(lrc_name)[0] + '.srt'

if srt_dir:
  srt_file = os.path.join(srt_dir, srt_name)
else:
  srt_file = srt_name

lyrics = {}
start_time = 0
with open(lrc_file, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.match(r'\[(\d+):(\d+).(\d+)\](.*)', line)
        if match:
            min, sec, ms = match.group(1, 2, 3)
            text = match.group(4)
            srt_timestamp = f'00:{min}:{sec},{ms}'
            print(srt_timestamp)
            if srt_timestamp in lyrics:
                lyrics[srt_timestamp].append(text)
            else:
                lyrics[srt_timestamp] = [text]


with open(srt_file, 'w', encoding='utf-8') as f:
    index = 1
    last_time_stamp = None
    last_text = None
    for timestamp in sorted(lyrics.keys()):
        if(last_time_stamp==None):
            last_time_stamp = timestamp
            last_text = '\n'.join(lyrics[timestamp])
            continue
        text = '\n'.join(lyrics[timestamp])
        f.write('{}\n{} --> {}\n{}\n\n'.format(index,
                last_time_stamp, timestamp, last_text))
        index += 1
        last_time_stamp = timestamp
        last_text = text



