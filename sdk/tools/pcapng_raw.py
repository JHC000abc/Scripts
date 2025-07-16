# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""
from pcapng.scanner import FileScanner
from pcapng.blocks import EnhancedPacket
from sdk.utils.util_cmd import RunCmd


def tran_pcapng_raw(in_file, out_file):
    """

    :param in_file:
    :param out_file:
    :return:
    """
    with open(in_file, 'rb') as fp, \
            open(out_file, 'wb') as audio_out:
        scanner = FileScanner(fp)
        for block in scanner:

            if isinstance(block, EnhancedPacket):
                frame = block.packet_data
                # print(len(b"33\x00\x02\x00\n\x00\x92}\x01\xdd@\x86\xdd"))

                # DIX Ethernet
                mac_frame_header = frame[:14]
                mac_frame_crc = frame[-4:]
                mac_payload = frame[14:]

                ethernet_type = mac_frame_header[-2:]

                if ethernet_type == b'\x86\xdd':  # ipv6
                    # 解析IPv6 报文头
                    # IPv6 基本报头 40 字节定长
                    ip_header = mac_payload[:40]
                    ip_payload_length = ip_header[4:6]
                    service_protocol = ip_header[6]

                    ip_packet_length = int.from_bytes(
                        ip_payload_length, byteorder='big')
                    ip_payload = mac_payload[40:ip_packet_length + 40]
                    # print(service_protocol)
                    if service_protocol == 0x11:  # UDP 17
                        udp_header = ip_payload[:8]
                        # UDP报头由4个域组成，其中每个域各占用2个字节，具体包括源端口号、目标端口号、数据包长度、校验值。
                        udp_payload_length = udp_header[4:6]

                        udp_packet_length = int.from_bytes(
                            udp_payload_length, byteorder='big')
                        # UDP数据报的长度(包括首部和数据)
                        udp_payload = ip_payload[8:udp_packet_length]

                        # 使用RTP协议解码
                        rtp_header = udp_payload[:12]
                        rtp_tag = rtp_header[0]

                        # 校验位
                        # print(rtp_tag)
                        if rtp_tag == 0x80:  # 128
                            rtp_payload_type = rtp_header[1]
                            # print(rtp_payload_type)
                            if rtp_payload_type == 0x7f:  # 127
                                # 用这个顺序号进行正向同步
                                rtp_sequence_number = int.from_bytes(
                                    rtp_header[2:4], byteorder='big')
                                rtp_timestamp = int.from_bytes(
                                    rtp_header[4:8], byteorder='big')
                                rtp_synchronization_source_identifier = int.from_bytes(
                                    rtp_header[9:12], byteorder='big')

                                rtp_payload = udp_payload[12:]

                                # 不同步的正向音频
                                audio_out.write(rtp_payload)

                                # print(f'Write RTP Sequence: {rtp_sequence_number}')
                #
                elif ethernet_type == b'\x86\x00':  # ipv4
                    print("IPv4 detected!")
                    pass
            # else:
            #     print("type(block)",type(block))


def tran_raw_mp4(ffmpeg_file, raw_file, mp4_file):
    """

    """

    cmd = R"{} -f h264 -i {} -vcodec copy {}".format(
        ffmpeg_file, raw_file, mp4_file)
    print(cmd)
    for info in RunCmd().run(cmd):
        pass
        # print(info)
    # os.system(cmd)
