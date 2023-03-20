import sys
import time
import logging
import csv
from datetime import datetime
from queue import Queue, Empty
from pc_ble_driver_py.observers import *

TARGET_DEV_NAME = "Gen2 Force Platform"
CONNECTIONS = 1
CFG_TAG = 1

CSV_LOG_FILE_NAME = "Gen2_Force_Platform.csv"

force1 = 0
force2 = 0
force3 = 0
CapTouch1 = 0
CapTouch2 = 0
Captouch3 = 0

def init(conn_ic_id):
    # noinspection PyGlobalUndefined
    global config, BLEDriver, BLEAdvData, BLEEvtID, BLEAdapter, BLEEnableParams, BLEGapTimeoutSrc, BLEUUID, BLEUUIDBase, BLEConfigCommon, BLEConfig, BLEConfigConnGatt, BLEGapScanParams, BLEConfigConnGap, BLEGapConnParams
    from pc_ble_driver_py import config

    config.__conn_ic_id__ = conn_ic_id
    # noinspection PyUnresolvedReferences
    from pc_ble_driver_py.ble_driver import (
        BLEDriver,
        BLEAdvData,
        BLEEvtID,
        BLEEnableParams,
        BLEGapTimeoutSrc,
        BLEUUID,
        BLEUUIDBase,
        BLEGapScanParams,
        BLEGapConnParams,
        BLEConfigCommon,
        BLEConfig,
        BLEConfigConnGatt,
        BLEConfigConnGap,
    )

    # noinspection PyUnresolvedReferences
    from pc_ble_driver_py.ble_adapter import BLEAdapter

    global nrf_sd_ble_api_ver
    nrf_sd_ble_api_ver = config.sd_api_ver_get()

class CsvWriter():
    def __init__(self):
        self.CsvFormat = {"Timestamp": None,
                          "Data": None,
                          "Length": None}
        self.keys = self.CsvFormat.keys()
        
        self.now = datetime.now()
        self.file_timestamp = self.now.strftime("%Y-%m-%d-%H-%M_") 
        self.csvfilename = self.file_timestamp + CSV_LOG_FILE_NAME
    
    def CsvCreateFile(self):
        with open(self.csvfilename, 'w', newline='') as csvfile:
            logwrite = csv.DictWriter(csvfile, self.keys)
            logwrite.writeheader()
    
    def CsvWriteFile(self, data, len):
        timestamp = datetime.now()
        new_row = self.CsvFormat
        new_row["Data"] = data
        new_row["Timestamp"] = timestamp.strftime("%M:%S.%f")
        new_row["Length"] = len
        with open(self.csvfilename, 'a', newline='') as csvfile:
            logwrite = csv.DictWriter(csvfile, self.keys)
            logwrite.writerow(new_row)



class NusCollector(BLEDriverObserver, BLEAdapterObserver):
    def __init__(self, adapter):
        super(NusCollector, self).__init__()
        self.adapter = adapter
        self.conn_q = Queue()
        self.adapter.observer_register(self)
        self.adapter.driver.observer_register(self)
        self.adapter.default_mtu = 247
        self.nus_base = BLEUUIDBase([
            0x6e, 0x40, 0x00, 0x00, 0xb5, 0xa3, 0xf3, 0x93, 0xe0, 0xa9, 0xe5, 0x0e, 0x24, 0xdc, 0xca, 0x9e
        ])
        self.nus_rx = BLEUUID(0x0002, self.nus_base)
        self.nus_tx = BLEUUID(0x0003, self.nus_base)

        # Create log file for data received from NUS peripheral
        self.csvwriter = CsvWriter()
        self.csvwriter.CsvCreateFile()
        

    def open(self):
        self.adapter.driver.open()
        gatt_cfg = BLEConfigConnGatt()
        gatt_cfg.att_mtu = self.adapter.default_mtu
        gatt_cfg.tag = CFG_TAG
        self.adapter.driver.ble_cfg_set(BLEConfig.conn_gatt, gatt_cfg)

        conn_cfg = BLEConfigConnGap()
        conn_cfg.conn_count = 1
        conn_cfg.event_length = 320
        self.adapter.driver.ble_cfg_set(BLEConfig.conn_gap, conn_cfg)

        self.adapter.driver.ble_enable()
        self.adapter.driver.ble_vs_uuid_add(self.nus_base)

    def close(self):
        self.adapter.driver.close()

    def connect_and_discover(self):
        scan_duration = 5
        scan_params = BLEGapScanParams(interval_ms=200, window_ms=150, timeout_s=scan_duration)
        message = "We are connected!\r\n"

        self.adapter.driver.ble_gap_scan_start(scan_params=scan_params)

        try:
            new_conn = self.conn_q.get(timeout=scan_duration)
            self.adapter.service_discovery(new_conn)
            self.adapter.enable_notification(new_conn, self.nus_tx)
            # Send BLE write command to NUS peripheral on connection
            # data = [ord(n) for n in list(message)]
            # self.adapter.write_cmd(new_conn, self.nus_rx, data)
            return new_conn
        except Empty:
            print("No device advertising with name {TARGET_DEV_NAME} found.")
            return None

    def on_gattc_evt_exchange_mtu_rsp(self, ble_driver, conn_handle, status, att_mtu):
        print("ATT MTU updated to {}".format(att_mtu))
    
    def on_gap_evt_data_length_update(
        self, ble_driver, conn_handle, data_length_params
    ):
        print("Max rx octets: {}".format(data_length_params.max_rx_octets))
        print("Max tx octets: {}".format(data_length_params.max_tx_octets))
        print("Max rx time: {}".format(data_length_params.max_rx_time_us))
        print("Max tx time: {}".format(data_length_params.max_tx_time_us))

    def on_gatts_evt_exchange_mtu_request(self, ble_driver, conn_handle, client_mtu):
        print("Client requesting to update ATT MTU to {} bytes".format(client_mtu))
    def on_gap_evt_connected(
        self, ble_driver, conn_handle, peer_addr, role, conn_params
    ):
        print("New connection: {}".format(conn_handle))
        self.conn_q.put(conn_handle)

    def on_gap_evt_disconnected(self, ble_driver, conn_handle, reason):
        print("Disconnected: {} {}".format(conn_handle, reason))

    def on_gap_evt_adv_report(
        self, ble_driver, conn_handle, peer_addr, rssi, adv_type, adv_data
    ):
        conn_params = BLEGapConnParams(min_conn_interval_ms=7.5, max_conn_interval_ms=7.5, conn_sup_timeout_ms=4000, slave_latency=0)
        
        if BLEAdvData.Types.complete_local_name in adv_data.records:
            dev_name_list = adv_data.records[BLEAdvData.Types.complete_local_name]

        elif BLEAdvData.Types.short_local_name in adv_data.records:
            dev_name_list = adv_data.records[BLEAdvData.Types.short_local_name]

        else:
            return

        dev_name = "".join(chr(e) for e in dev_name_list)
        address_string = "".join("{0:02X}".format(b) for b in peer_addr.addr)
        print(
            "Received advertisment report, address: 0x{}, device_name: {}".format(
                address_string, dev_name
            )
        )

        if dev_name == TARGET_DEV_NAME:
            self.adapter.connect(peer_addr, conn_params = conn_params, tag=CFG_TAG)

    def on_notification(self, ble_adapter, conn_handle, uuid, data):
        global force1
        global force2
        global force3
        global CapTouch1
        global CapTouch2
        global Captouch3

        #convert 2s complement binary to decimal for the 3 force readings
        force1 = data[0]                            #high byte for the force reading 
        force1 = (force1 << 8) + data[1]            #low byte for the force reading 
        if(force1 & 0x8000):
            force1 = (force1 & 0x7FFF) - 32768      #if 2s complement value is negative convert to appropriate decimal value

        force2 = data[2]
        force2 = (force2 << 8) + data[3]
        if(force2 & 0x8000):
            force2 = (force2 & 0x7FFF) - 32768


        force3 = data[4]
        force3 = (force3 << 8) + data[5]
        if(force3 & 0x8000):
            force3 = (force3 & 0x7FFF) - 32768

        CapTouch1 = data[6]
        CapTouch2 = data[7]
        Captouch3 = data[8]

        #print("Connection: {}, {} = {}, {}".format(conn_handle, uuid, data, force))
        self.csvwriter.CsvWriteFile(''.join("{:02x}".format(octet,'x') for octet in data), len(data))


def main(selected_serial_port, q_force):
    init("NRF52")
    print("Serial port used: {}".format(selected_serial_port))
    driver = BLEDriver(
        serial_port=selected_serial_port, auto_flash=False, baud_rate=1000000, log_severity_level="info"
    )

    adapter = BLEAdapter(driver)
    collector = NusCollector(adapter)
    collector.open()
    conn = collector.connect_and_discover()
    
    global force1
    global force2
    global force3
    global CapTouch1
    global CapTouch2
    global Captouch3


    while conn is not None:
        time.sleep(0.0015)
        #print("Force is {}".format(force))
        q_force.put([force1, force2, force3, CapTouch1, CapTouch2, Captouch3])

    collector.close()


def item_choose(item_list):
    for i, it in enumerate(item_list):
        print("\t{} : {}".format(i, it))
    print(" ")

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if (choice >= 0) and (choice < len(item_list)):
                break
        except Exception:
            pass
        print("\tTry again...")
    return choice


if __name__ == "__main__":
    #logging.basicConfig(
    #    level="DEBUG",
    #   format="%(asctime)s [%(thread)d/%(threadName)s] %(message)s",
    #)
    serial_port = None
    if len(sys.argv) < 2:
        print("Please specify a serial port for the connectivity IC (COMx, /dev/ttyACMx, or /dev/tty.usbmodem.x depending on the OS)")
        exit(1)
    init("NRF52")
    if len(sys.argv) == 2:
        serial_port = sys.argv[1]
    else:
        descs = BLEDriver.enum_serial_ports()
        choices = ["{}: {}".format(d.port, d.serial_number) for d in descs]
        choice = item_choose(choices)
        serial_port = descs[choice].port
    main(serial_port)
    quit()
