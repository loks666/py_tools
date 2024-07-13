import ctypes
import os
import time
from ctypes import *

import numpy as np
from pykalman import KalmanFilter

VCI_USBCAN2 = 4
STATUS_OK = 1


class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)]


class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte * 8),
                ("Reserved", c_ubyte * 3)]


class VCI_CAN_OBJ_ARRAY(Structure):
    _fields_ = [('SIZE', c_uint16), ('STRUCT_ARRAY', POINTER(VCI_CAN_OBJ))]

    def __init__(self, num_of_structs):
        self.STRUCT_ARRAY = cast((VCI_CAN_OBJ * num_of_structs)(), POINTER(VCI_CAN_OBJ))
        self.SIZE = num_of_structs
        self.ADDR = self.STRUCT_ARRAY[0]


def main_logic(log_signal, is_running):
    dll_path = os.path.join(os.path.dirname(__file__), 'ControlCAN.dll')
    canDLL = ctypes.windll.LoadLibrary(dll_path)
    ret = canDLL.VCI_OpenDevice(VCI_USBCAN2, 0, 0)
    if ret == STATUS_OK:
        log_signal.emit('调用 VCI_OpenDevice成功')
    else:
        log_signal.emit('调用 VCI_OpenDevice出错')

    vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 0, 0, 0x00, 0x1C, 0)
    ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 0, byref(vci_initconfig))
    if ret == STATUS_OK:
        log_signal.emit('调用 VCI_InitCAN1成功')
    else:
        log_signal.emit('调用 VCI_InitCAN1出错')

    ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 0)
    if ret == STATUS_OK:
        log_signal.emit('调用 VCI_StartCAN1成功')
    else:
        log_signal.emit('调用 VCI_StartCAN1出错')

    ret = canDLL.VCI_InitCAN(VCI_USBCAN2, 0, 1, byref(vci_initconfig))
    if ret == STATUS_OK:
        log_signal.emit('调用 VCI_InitCAN2成功')
    else:
        log_signal.emit('调用 VCI_InitCAN2出错')

    ret = canDLL.VCI_StartCAN(VCI_USBCAN2, 0, 1)
    if ret == STATUS_OK:
        log_signal.emit('调用 VCI_StartCAN2成功')
    else:
        log_signal.emit('调用 VCI_StartCAN2出错')

    rx_vci_can_obj = VCI_CAN_OBJ_ARRAY(2500)
    typeDict = {'0x018': '加速度', '0x028': '角速度', '0x038': '欧拉角', '0x048': '四元数', '0x068': '气压'}
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    f = open('log_' + current_time + '.txt', 'a+')
    logs_ltr_statue = []

    try:
        threth = 45
        ltrs = []
        statue = 0

        while is_running():
            ret = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(rx_vci_can_obj.ADDR), 2500, 0)
            aflag, wflag, thflag = 0, 0, 0

            if ret > 0:
                for i in range(ret):
                    canData = rx_vci_can_obj.STRUCT_ARRAY[i]
                    ID = '0x{:04X}'.format(canData.ID)
                    dataType = typeDict.get(ID[:5], '未知')

                    if dataType == '加速度':
                        ax = canData.Data[1] * 16 + canData.Data[0]
                        ay = canData.Data[3] * 16 + canData.Data[2]
                        az = canData.Data[5] * 16 + canData.Data[4]
                        cAy = ax * 0.001
                        aflag = 1
                        f.write(f'设备号: {ID[-1]} ax: {ax} ay: {ay} az: {az}\n')
                    elif dataType == '角速度':
                        wx = 0.1 * (canData.Data[1] * 256 + canData.Data[0])
                        wy = 0.1 * (canData.Data[3] * 256 + canData.Data[2])
                        wz = 0.1 * (canData.Data[5] * 256 + canData.Data[4])
                        cWz = wz * 0.001
                        wflag = 1
                        f.write(f'设备号: {ID[-1]} wx: {wx} wy: {wy} wz: {wz}\n')
                    elif dataType == '欧拉角':
                        thx = 0.01 * (canData.Data[1] * 256 + canData.Data[0])
                        thy = 0.01 * (canData.Data[3] * 256 + canData.Data[2])
                        thz = 0.01 * (canData.Data[5] * 256 + canData.Data[4])
                        cThz = thz * 0.001
                        thflag = 1
                        f.write(f'设备号: {ID[-1]} thx: {thx} thy: {thy} thz: {thz}\n')
                    elif dataType == '四元数':
                        qw = 0.0001 * (canData.Data[1] * 256 + canData.Data[0])
                        qx = 0.0001 * (canData.Data[3] * 256 + canData.Data[2])
                        qy = 0.0001 * (canData.Data[5] * 256 + canData.Data[4])
                        qz = 0.0001 * (canData.Data[7] * 256 + canData.Data[6])
                        f.write(f'设备号: {ID[-1]} qw: {qw} qx: {qx} qy: {qy} qz: {qz}\n')
                    elif dataType == '气压':
                        gp = canData.Data[1] * 256 + canData.Data[0]
                        f.write(f'设备号: {ID[-1]} 气压: {gp}\n')

                if aflag and wflag and thflag:
                    ms, mu, B, H, hx, Kfi, Cfi, g = 46448, 17600, 2.56, 1.36, 0.782, 100000, 102000, 9.8
                    ltr = 2 * (Kfi * cThz + Cfi * cWz + ms * cAy * (H - hx)) / ((ms + mu) * g * B)
                    if ltr < 1:
                        ltrs.append(ltr)
                    aflag, wflag, thflag = 0, 0, 0

                if len(ltrs) >= 20:
                    ltrs.pop(0)
                    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
                    (filtered_state_means, filtered_state_covariances) = kf.filter(ltrs)
                    (filtered_state_means_pred, filtered_state_covariances_pred) = kf.smooth(ltrs)
                    n, ltime = 1, 0

                    while True:
                        (filtered_state_means_pred, filtered_state_covariances_pred) = kf.filter_update(
                            filtered_state_means_pred[-1], filtered_state_covariances_pred[-1])

                        if filtered_state_means_pred[-1] > 0.85:
                            statue = 1
                            ltime = n * 0.1
                            log_signal.emit(f'-----{ltime:.1f} s 后将会侧翻！！----')

                        if n >= 100:
                            ltime = 0
                            log_signal.emit('--------不会侧翻--------')
                            statue = 0
                            break

                        ltr_value = filtered_state_means_pred[-1] if not isinstance(filtered_state_means_pred[-1],
                                                                                    np.ndarray) else \
                        filtered_state_means_pred[-1][0]
                        logs_ltr_statue.append([ltr_value, statue, ltime])
                        n += 1

    except Exception as e:
        log_signal.emit(f'发生异常: {str(e)}')
        logs_ltr_statue = np.array(logs_ltr_statue)
        np.savetxt('ltr_statue.txt', logs_ltr_statue)
        canDLL.VCI_CloseDevice(VCI_USBCAN2, 0)
    finally:
        canDLL.VCI_CloseDevice(VCI_USBCAN2, 0)
