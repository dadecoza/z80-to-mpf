import wave
import struct
import math
import numpy
import sys

sample_rate = 44100.0
amplitude = 30000


def square(freq, t):
    w = 2 * math.pi * freq
    return int(amplitude*numpy.sign(math.sin(w*t)))


def tone(freq, cycles):
    values = []
    for i in range(int((sample_rate/freq)*(cycles))):
        t = float(i) / (float(sample_rate))
        value = square(freq, t)
        values.append(value)
    return values


def synctone(freq, seconds):
    values = []
    for i in range(int(sample_rate*seconds)):
        t = float(i) / (float(sample_rate))
        value = square(freq, t)
        values.append(value)
    return values


def leadsync():
    return synctone(1000, 4)


def sync():
    return synctone(2000, 2)


def tone1k(cycles):
    return tone(1000, cycles)


def tone2k(cycles):
    return tone(2000, cycles)


def checksum(data):
    return sum(data) & 255


def bit(value):
    return tone2k(4)+tone1k(4) if value else tone2k(8)+tone1k(2)


def btone(bt):
    zero = bit(0)
    one = bit(1)
    values = []
    values += zero                                # start
    values += one if (bt & 0b00000001) else zero  # bit 0
    values += one if (bt & 0b00000010) else zero  # bit 1
    values += one if (bt & 0b00000100) else zero  # bit 2
    values += one if (bt & 0b00001000) else zero  # bit 3
    values += one if (bt & 0b00010000) else zero  # bit 4
    values += one if (bt & 0b00100000) else zero  # bit 5
    values += one if (bt & 0b01000000) else zero  # bit 6
    values += one if (bt & 0b10000000) else zero  # bit 7
    values += one                                 # stop
    return values


def load_z80_file(filename):
    fh = open(filename, "rb")
    z80data = fh.read()
    fh.close()
    data = z80data[10:]
    startaddress = int.from_bytes(z80data[8:10], "little")
    endaddress = startaddress+len(data)-1
    return {
        "start": startaddress,
        "end": endaddress,
        "data": data,
        "filename": filename
    }


def create_wave_values(z80):
    data = z80["data"]
    filename_high = 0x12
    filename_low = 0x34
    start_high, start_low = z80["start"].to_bytes(2, 'big')
    end_high, end_low = z80["end"].to_bytes(2, 'big')
    cs = checksum(data)
    values = []
    values += leadsync()
    values += btone(filename_low)
    values += btone(filename_high)
    values += btone(start_low)
    values += btone(start_high)
    values += btone(end_low)
    values += btone(end_high)
    values += btone(cs)
    values += sync()
    for bt in data:
        values += btone(bt)
    values += sync()
    return values


def write_wav_file(filename, values):
    file = wave.open(filename, 'wb')
    file.setnchannels(1)
    file.setsampwidth(2)
    file.setframerate(sample_rate)
    for value in values:
        data = struct.pack('<h', value)
        file.writeframesraw(data)
    file.close()


def create_srecord(address, data):
    address_high, address_low = address.to_bytes(2, 'big')
    data_size = len(data)
    record_type = 0
    record_data = [
        data_size,
        address_high,
        address_low,
        record_type
    ]
    record_data += data
    record_data.append((-sum(record_data)) & 0x0FF)
    str_data = "".join([format(b, '02X') for b in record_data])
    return ":%s\n" % str_data


def create_srecords(z80data):
    buffer = []
    data = z80data["data"]
    start = z80data["start"]
    srsize = 8
    srecords = []
    address = start
    for i in range(len(data)):
        buffer.append(data[i])
        if not ((i+1) % srsize):
            srecords.append(create_srecord(address, buffer))
            buffer.clear()
            address += srsize
    srecords.append(create_srecord(address, buffer))
    srecords.append(":00000001FF\n")
    return srecords


def write_intel_hex_file(filename, srecords):
    fh = open(filename, "w")
    for r in srecords:
        fh.write(r)
    fh.close()


def write_files(filename):
    name, ext = filename.split(".")
    if ext != "z80":
        print("Expected .z80 file")
        sys.exit(0)
    wav_filename = "%s.wav" % name
    hex_filename = "%s.hex" % name
    print("Loading %s ..." % filename)
    data = load_z80_file(filename)
    print("Creating Intel Hex file ...")
    srecords = create_srecords(data)
    write_intel_hex_file(hex_filename, srecords)
    print("Creating WAV file ...")
    values = create_wave_values(data)
    write_wav_file(wav_filename, values)
    print("All done!")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s filename.z80" % sys.argv[0])
        sys.exit(0)
    filename = sys.argv[1]
    write_files(filename)
