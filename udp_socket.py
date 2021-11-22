# Based on: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry (Apache License 2.0)

import time


class UdpSocket():
    def __init__(self, udp_ip, send_port, receive_port, enable_receive=True, suppress_warnings=False):

        import socket

        self.udp_ip = udp_ip
        self.udp_send_port = send_port
        self.udp_receive_port = receive_port
        self.enable_receive = enable_receive
        self.suppress_warnings = suppress_warnings  # when true warnings are suppressed
        self.is_data_received = False
        self.data_rx = None

        # Connect via UDP
        # internet protocol, udp (DGRAM) socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # allows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state waiting for late packets to arrive.
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind((udp_ip, receive_port))

        # Create Receiving thread if required
        if enable_receive:
            import threading
            self.receive_thread = threading.Thread(
                target=self.read_udp_thread, daemon=True)
            self.receive_thread.start()

    def __del__(self):
        self.close_socket()

    def close_socket(self):
        # Function to close socket
        self.udp_socket.close()

    def send_data(self, str):
        # Use this function to send string to C#
        self.udp_socket.sendto(bytes(str, 'utf-8'),
                               (self.udp_ip, self.udp_send_port))

    def receive_data(self):
        """
        Should not be called by user
        Function BLOCKS until data is returned from C#. It then attempts to convert it to string and returns on successful conversion.
        An warning/error is raised if:
            - Warning: Not connected to C# application yet. Warning can be suppressed by setting suppressWarning=True in constructor
            - Error: If data receiving procedure or conversion to string goes wrong
            - Error: If user attempts to use this without enabling RX
        :return: returns None on failure or the received string on success
        """
        if not self.enable_receive:  # if RX is not enabled, raise error
            raise ValueError(
                "Attempting to receive data without enabling this setting. Ensure this is enabled from the constructor")

        data = None
        try:
            data, _ = self.udp_socket.recvfrom(1024)
            data = data.decode('utf-8')
        except OSError as e:
            if e.winerror == 10054:  # An error occurs if you try to receive before connecting to other application
                if not self.suppress_warnings:
                    print("Are You connected to the other application? Connect to it!")
                else:
                    pass
            else:
                raise ValueError(
                    "Unexpected Error. Are you sure that the received data can be converted to a string")

        return data

    def read_udp_thread(self):  # Should be called from thread
        """
        This function should be called from a thread [Done automatically via constructor]
                (import threading -> e.g. udpReceiveThread = threading.Thread(target=self.ReadUdpNonBlocking, daemon=True))
        This function keeps looping through the BLOCKING ReceiveData function and sets self.dataRX when data is received and sets received flag
        This function runs in the background and updates class variables to read data later

        """

        self.is_data_received = False  # Initially nothing received

        while True:
            # Blocks (in thread) until data is returned (OR MAYBE UNTIL SOME TIMEOUT AS WELL)
            data = self.receive_data()
            self.data_received = data  # Populate AFTER new data is received
            self.is_data_received = True
            # When it reaches here, data received is available

    def read_received_data(self):
        """
        This is the function that should be used to read received data
        Checks if data has been received SINCE LAST CALL, if so it returns the received string and sets flag to False (to avoid re-reading received data)
        data is None if nothing has been received
        :return:
        """

        data = None

        if self.is_data_received:  # if data has been received
            self.is_data_received = False
            data = self.data_received
            self.data_received = None  # Empty receive buffer

        return data


def main():
    print("UDP Module")

    # Create UDP socket to use for sending (and receiving)
    socket = UdpSocket(udp_ip="127.0.0.1", send_port=8000, receive_port=8001,
                       enable_receive=True, suppress_warnings=False)

    while True:

        data = socket.read_received_data()

        if data != None:  # if NEW data has been received since last ReadReceivedData function call
            print(data)  # print new received data
            socket.send_data("Sent from server")

        time.sleep(0.01)


if __name__ == "__main__":
    main()
