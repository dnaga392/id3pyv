# import chardet
# import sys
# from mutagen.easyid3 import EasyID3
# from mutagen.id3 import ID3


# path = "01-Old town.mp3"


class ID3v2Frame(object):
    def __init__(self):
        self.id = ''
        self.size = 0
        self.flags = int(0).to_bytes(2, 'big')
        self.info = None


class ID3v2(object):
    def __init__(self):
        self.identifier = ''
        self.version = (0, 0)
        self.flags = int(0).to_bytes(1, 'big')
        self.size = 0
        self.frames = []


# def test_easy_id3():
#     tags = EasyID3(path)
#     print(tags.pprint())
#     # print(dir(tags))
#     print(tags['album'])
#     print(type(tags['album']))
#     print(tags['album'][0])
#     print(type(tags['album'][0]))
#     # title = tags['album'][0]
#     # print(tags['album'][0].encode())
#     # print(bytes(tags['album'][0], 'ascii'))
#     # print(tags['album'][0].encode('utf-8').decode('cp932'))
#     # print(chardet.detect(title.encode('utf-16')))


# def test_id3():
#     # tags = ID3(path)
#     tags = ID3()
#     # print(dir(tags))
#     # print(help(tags.load))
#     tags.load(path, v2_version=3)
#     print(tags.pprint())


def read_id3v2_4(fp):
    """
     The bitorder in ID3v2 is most significant bit first (MSB). The
    byteorder in multibyte numbers is most significant byte first (e.g.
    $12345678 would be encoded $12 34 56 78), also known as big endian
    and network byte order.

    Overall tag structure:

      +-----------------------------+
      |      Header (10 bytes)      |
      +-----------------------------+
      |       Extended Header       |
      | (variable length, OPTIONAL) |
      +-----------------------------+
      |   Frames (variable length)  |
      +-----------------------------+
      |           Padding           |
      | (variable length, OPTIONAL) |
      +-----------------------------+
      | Footer (10 bytes, OPTIONAL) |
      +-----------------------------+
    """
    flags = fp.read(1)
    # print("ID3v2 flags:", flags)
    print("ID3v2 flags:")
    a, b, c, d, _, _, _, _ = [int(x) for x in format(flags[0], '08b')]
    print("  a - Unsynchronisation     :", a)
    print("  b - Extended header       :", b)
    print("  c - Experimental indicator:", c)
    print("  d - Footer present        :", d)
    # print("ID3v2 size:", fp.read(1), fp.read(1), fp.read(1), fp.read(1))
    id3v2_size = int.from_bytes(fp.read(4), 'big')
    print("ID3v2 size [bytes]:", id3v2_size)
    id3v2_size -= 10

    # 3.2. Extended header
    if b:
        # TODO: Write code to read Extended Header
        assert False, "This music file has Extended Header!"

    # 4. ID3v2 frame overview
    while id3v2_size > 0:
        # print("ID3v2 size:", fp.read(1), fp.read(1), fp.read(1), fp.read(1))
        frame_id = fp.read(4)
        if not int.from_bytes(frame_id, 'big'):
            break;
        frame_id = frame_id.decode()
        print("ID3v2 frame, Frame ID:", frame_id)
        frame_size = int.from_bytes(fp.read(4), 'big')
        print("ID3v2 frame, Size:", frame_size)
        print("ID3v2 frame, Flags:")
        _, a, b, c, _, _, _, _ = [int(x) for x in format(fp.read(1)[0], '08b')]
        _, h, _, _, k, m, n, p = [int(x) for x in format(fp.read(1)[0], '08b')]
        """4.1.1. Frame status flags"""
        # print("  Frame status flags")
        print("  a - Tag alter preservation :", a)
        print("  b - File alter preservation:", b)
        print("  c - Read only              :", c)
        """4.1.2. Frame format flags"""
        # print("  Frame format flags")
        print("  h - Grouping identity      :", h)
        print("  k - Compression            :", k)
        print("  m - Encryption             :", m)
        print("  n - Unsynchronisation      :", n)
        print("  p - Data length indicator  :", p)
        id3v2_size -= 10
        frame_info = fp.read(frame_size)
        # print(frame_info)
        frame_encoding = frame_info[0]
        frame_info = frame_info[1:]
        print(format(frame_encoding, '02x'))
        # print(frame_info)
        # encoding_map = {'00': 'ISO-8859-1',
        #                 '01': 'UTF-16',
        #                 '02': 'UTF-16BE',
        #                 '03': 'UTF-8'}
        encoding_map = {'00': 'cp932',
                        '01': 'UTF-16',
                        '02': 'UTF-16BE',
                        '03': 'UTF-8'}
        # print(frame_info.decode(encoding_map[format(frame_encoding, '02x')]))
        print(frame_info)
        if frame_id == 'TALB':
            talb_info = frame_info
        id3v2_size -= frame_size

    print("Padding [bytes]:", id3v2_size)

    print(talb_info)
    # print(talb_info.decode('cp932'))
    # print(talb_info.decode('cp1252'))


def read_raw_id3(path):
    id3v2 = ID3v2()
    with open(path, mode='rb') as fp:
        # 3.1. ID3v2 header
        """
        The ID3v2 tag header, which should be the first information in the
        file, is 10 bytes as follows:

          ID3v2/file identifier      "ID3"
          ID3v2 version              $03 00
          ID3v2 flags                %abc00000
          ID3v2 size             4 * %0xxxxxxx
        """

        identifier = fp.read(3).decode()
        if identifier != 'ID3':
            print("ID3v2 is nothing!")
            return
        print("ID3v2/file identifier: `{}`".format(identifier))
        id3v2.identifier = identifier

        # v1 = int.from_bytes(fp.read(1), 'big')
        # v2 = int.from_bytes(fp.read(1), 'big')
        # print("ID3v2 version: {0}.{1}".format(v1, v2))
        # id3v2.version = (v1, v2)
        v = tuple([int(format(x, '08b'), 2) for x in fp.read(2)])
        print("ID3v2 version: {0}.{1}".format(*v))
        id3v2.version = v

        print("ID3v2 flags:")
        flags = fp.read(1)
        id3v2.flags = flags
        a, b, c, _, _, _, _, _ = [int(x) for x in format(flags[0], '08b')]
        print("  a - Unsynchronisation     :", a)
        print("  b - Extended header       :", b)
        print("  c - Experimental indicator:", c)
        # id3v2_size = int.from_bytes(fp.read(4), 'big')
        bits = [format(x, '08b') for x in fp.read(4)]
        id3v2_size = int(''.join([x[1:] for x in bits]), 2)
        id3v2.size = id3v2_size
        print("ID3v2 size [bytes]:", id3v2_size)
        print("  ID3v2 size (bits) [bytes]:", ' '.join(bits))
        # id3v2_size -= 10
        # print("-- ID3v2 size (After tag header) [bytes]:", id3v2_size)

        # 3.3. ID3v2 frame overview
        while id3v2_size > 0:
            frame = ID3v2Frame()
            frame_id = fp.read(4)
            if not int.from_bytes(frame_id, 'big'):
                # 読んだ分の位置を戻す
                fp.seek(fp.tell() - 4)
                break;
            frame_id = frame_id.decode()
            frame.id = frame_id
            print("ID3v2 frame, Frame ID:", frame_id)
            frame_size = int.from_bytes(fp.read(4), 'big')
            frame.size = frame_size
            print("ID3v2 frame, Size:", frame_size)
            # 3.3.1. Frame header flags
            print("ID3v2 frame, Flags:")
            frame_flags = fp.read(2)
            frame.flags = frame_flags
            a, b, c, _, _, _, _, _ = [int(x) for x in format(frame_flags[0], '08b')]
            i, j, k, _, _, _, _, _ = [int(x) for x in format(frame_flags[1], '08b')]
            print("  a - Tag alter preservation :", a)
            print("  b - File alter preservation:", b)
            print("  c - Read only              :", c)
            print("  i - Compression            :", i)
            print("  j - Encryption             :", j)
            print("  k - Grouping identity      :", k)
            id3v2_size -= 10
            print("-- ID3v2 size (After frame header) [bytes]:", id3v2_size)

            print("ID3v2 frame, Information:")
            frame_info = fp.read(frame_size)
            frame.info = frame_info
            id3v2_size -= frame_size
            print("-- ID3v2 size (After frame info) [bytes]:", id3v2_size)

            if frame_id[0] == 'T':
                # 4.2.   Text information frames
                text_encoding = frame_info[0]
                frame_info = frame_info[1:]
                print("  Text encoding:", format(text_encoding, '02x'))
                encoding_map = {'00': 'cp932',
                                '01': 'UTF-16'}
                print("  information:", frame_info.decode(encoding_map[format(text_encoding, '02x')]))
            elif frame.id == 'APIC':
                text_encoding = frame.info[0]
                frame_info = frame.info[1:]
                print('  Text encoding', format(text_encoding, '02x'))
                mime_type, frame_info = frame_info.split(int(0).to_bytes(1, 'big'), 1)
                # mime_type = bytearray(mime_type)
                # mime_type.append(int(0).to_bytes(1, 'big')[0])
                # mime_type = bytes(mime_type)
                print('  MIME type', mime_type.decode())
                picture_type = frame_info[0]
                frame_info = frame_info[1:]
                print('  Picture type', format(picture_type, '02x'))
                description, picture_data = frame_info.split(int(0).to_bytes(1, 'big'), 1)
                encoding_map = {'00': 'cp932',
                                '01': 'UTF-16'}
                description = description.decode(encoding_map[format(text_encoding, '02x')])
                # description = bytearray(description)
                # description.append(int(0).to_bytes(1, 'big')[0])
                # description = bytes(description)
                print('  Description', description)
                print('  Picture data', picture_data[:10])
            else:
                # print("  information:", frame_info)
                pass
            id3v2.frames.append(frame)

        print("Padding [bytes]:", id3v2_size)
        while id3v2_size:
            b = fp.read(1)
            if int.from_bytes(b, 'big'):
                print('invalid padding:', fp.tell() -1, b, id3v2_size)
                # 読んだ分の位置を戻す
                fp.seek(fp.tell() - 1)
                break;
            id3v2_size -= 1
        print("Padding [bytes]:", id3v2_size)
        over = 0
        while not int.from_bytes(fp.read(1), 'big'):
            over += 1
        fp.seek(fp.tell() - 1)  # 条件で読んだ分の位置を戻す
        print("Over Padding [bytes]:", over)
        print('mp3 data', fp.read(10))
    return id3v2

# if __name__ == '__main__':
#     # import locale
#     # print(locale.getdefaultlocale())
#     # When 'Language for non-Unicode programs' is 'English (United States)', => ('ja_JP', 'cp1252')
#     # When 'Language for non-Unicode programs' is 'Japanese (Japan)', => ('ja_JP', 'cp932')
# 
#     # test_easy_id3()
#     # test_id3()
#     # id3 = read_raw_id3(path)
