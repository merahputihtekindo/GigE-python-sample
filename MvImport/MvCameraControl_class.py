# -- coding: utf-8 --

import sys
import copy
import ctypes
import os

from ctypes import *
from CameraParams_const import *
from CameraParams_header import *
from MvCameraControl_header import *
from MvErrorDefine_const import *
from PixelType_const import *
from PixelType_header import *

MvCamCtrldll = ctypes.cdll.LoadLibrary(os.getenv('MVCAM_COMMON_RUNENV') + "/64/libMvCameraControl.so")

# used for callback function in camera instance
class _MV_PY_OBJECT_(Structure):
    pass
_MV_PY_OBJECT_._fields_ = [
    ('PyObject', py_object),
]
MV_PY_OBJECT = _MV_PY_OBJECT_

class MvCamera():

    def __init__(self):
        self._handle = c_void_p()  # record handle of connected device
        self.handle = pointer(self._handle)  # create handle pointer

    # Find Device
    @staticmethod
    def MV_CC_EnumDevices(nTLayerType, stDevList):
        MvCamCtrldll.MV_CC_EnumDevices.argtype = (c_uint, c_void_p)
        MvCamCtrldll.MV_CC_EnumDevices.restype = c_uint
        return MvCamCtrldll.MV_CC_EnumDevices(c_uint(nTLayerType), byref(stDevList))

    # Create Device Handle
    def MV_CC_CreateHandle(self, stDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandle.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandle.restype = c_uint
        return MvCamCtrldll.MV_CC_CreateHandle(byref(self.handle), byref(stDevInfo))

    #Create Device Handle without log
    def MV_CC_CreateHandleWithoutLog(self, stDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandleWithoutLog.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandleWithoutLog.restype = c_uint
        return MvCamCtrldll.MV_CC_CreateHandleWithoutLog(byref(self.handle), byref(stDevInfo))

    #Destroy Device Handle
    def MV_CC_DestroyHandle(self):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        return MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

    #Open Device
    def MV_CC_OpenDevice(self, nAccessMode=MV_ACCESS_Exclusive, nSwitchoverKey=0):
        MvCamCtrldll.MV_CC_OpenDevice.argtype = (c_void_p, c_uint32, c_uint16)
        MvCamCtrldll.MV_CC_OpenDevice.restype = c_uint
        return MvCamCtrldll.MV_CC_OpenDevice(self.handle, nAccessMode, nSwitchoverKey)

    #Close Device
    def MV_CC_CloseDevice(self):
        MvCamCtrldll.MV_CC_CloseDevice.argtype = c_void_p
        MvCamCtrldll.MV_CC_CloseDevice.restype = c_uint
        return MvCamCtrldll.MV_CC_CloseDevice(self.handle)

    #Register the image callback function
    def MV_CC_RegisterImageCallBackEx(self, CallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterImageCallBackEx.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterImageCallBackEx.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterImageCallBackEx(self.handle, CallBackFun, pUser)

    #Start Grabbing
    def MV_CC_StartGrabbing(self):
        MvCamCtrldll.MV_CC_StartGrabbing.argtype = c_void_p
        MvCamCtrldll.MV_CC_StartGrabbing.restype = c_uint
        return MvCamCtrldll.MV_CC_StartGrabbing(self.handle)

    # Stop Grabbing
    def MV_CC_StopGrabbing(self):
        MvCamCtrldll.MV_CC_StopGrabbing.argtype = c_void_p
        MvCamCtrldll.MV_CC_StopGrabbing.restype = c_uint
        return MvCamCtrldll.MV_CC_StopGrabbing(self.handle)

    # Timeout mechanism is used to get image, and the SDK waits inside until the data is returned
    def MV_CC_GetOneFrameTimeout(self, pData, nDataSize, stFrameInfo, nMsec=1000):
        MvCamCtrldll.MV_CC_GetOneFrameTimeout.argtype = (c_void_p, c_void_p, c_uint, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetOneFrameTimeout.restype = c_uint
        return MvCamCtrldll.MV_CC_GetOneFrameTimeout(self.handle, pData, nDataSize, byref(stFrameInfo), nMsec)

    # Get Integer value
    def MV_CC_GetIntValue(self, strKey, stIntValue):
        MvCamCtrldll.MV_CC_GetIntValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetIntValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetIntValue(self.handle, strKey.encode('ascii'), byref(stIntValue))
    
    # Set Integer value
    def MV_CC_SetIntValue(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetIntValue.argtype = (c_void_p, c_void_p, c_uint32)
        MvCamCtrldll.MV_CC_SetIntValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetIntValue(self.handle, strKey.encode('ascii'), c_uint32(nValue))

    # Get Enum value
    def MV_CC_GetEnumValue(self, strKey, stEnumValue):
        MvCamCtrldll.MV_CC_GetEnumValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetEnumValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetEnumValue(self.handle, strKey.encode('ascii'), byref(stEnumValue))

    # Set Enum value
    def MV_CC_SetEnumValue(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetEnumValue.argtype = (c_void_p, c_void_p, c_uint32)
        MvCamCtrldll.MV_CC_SetEnumValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetEnumValue(self.handle, strKey.encode('ascii'), c_uint32(nValue))

    # Get Float value
    def MV_CC_GetFloatValue(self, strKey, stFloatValue):
        MvCamCtrldll.MV_CC_GetFloatValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetFloatValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetFloatValue(self.handle, strKey.encode('ascii'), byref(stFloatValue))

    # Set float value
    def MV_CC_SetFloatValue(self, strKey, fValue):
        MvCamCtrldll.MV_CC_SetFloatValue.argtype = (c_void_p, c_void_p, c_float)
        MvCamCtrldll.MV_CC_SetFloatValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetFloatValue(self.handle, strKey.encode('ascii'), c_float(fValue))

    # Get Boolean value
    def MV_CC_GetBoolValue(self, strKey, BoolValue):
        MvCamCtrldll.MV_CC_GetBoolValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetBoolValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetBoolValue(self.handle, strKey.encode('ascii'), byref(BoolValue))

    # Set Boolean value
    def MV_CC_SetBoolValue(self, strKey, bValue):
        MvCamCtrldll.MV_CC_SetBoolValue.argtype = (c_void_p, c_void_p, c_bool)
        MvCamCtrldll.MV_CC_SetBoolValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetBoolValue(self.handle, strKey.encode('ascii'), bValue)

    # Get String value
    def MV_CC_GetStringValue(self, strKey, StringValue):
        MvCamCtrldll.MV_CC_GetStringValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetStringValue.restype = c_uint
        return MvCamCtrldll.MV_CC_GetStringValue(self.handle, strKey.encode('ascii'), byref(StringValue))
    
    # Set String value
    def MV_CC_SetStringValue(self, strKey, sValue):
        MvCamCtrldll.MV_CC_SetStringValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetStringValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetStringValue(self.handle, strKey.encode('ascii'), sValue.encode('ascii'))
    
    # Send Command
    def MV_CC_SetCommandValue(self, strKey):
        MvCamCtrldll.MV_CC_SetCommandValue.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetCommandValue.restype = c_uint
        return MvCamCtrldll.MV_CC_SetCommandValue(self.handle, strKey.encode('ascii'))

    # Register Exception Message CallBack, call after open device
    def MV_CC_RegisterExceptionCallBack(self, ExceptionCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterExceptionCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterExceptionCallBack.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterExceptionCallBack(self.handle, ExceptionCallBackFun, pUser)

    # Register single event callback, which is called after the device is opened
    def MV_CC_RegisterEventCallBackEx(self, pEventName, EventCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterEventCallBackEx.argtype = (c_void_p, c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterEventCallBackEx.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterEventCallBackEx(self.handle, pEventName.encode('ascii'), EventCallBackFun, pUser)

    # Force IP
    def MV_GIGE_ForceIpEx(self, nIP, nSubNetMask, nDefaultGateWay):
        MvCamCtrldll.MV_GIGE_ForceIpEx.argtype = (c_void_p, c_uint, c_uint, c_uint)
        MvCamCtrldll.MV_GIGE_ForceIpEx.restype = c_uint
        return MvCamCtrldll.MV_GIGE_ForceIpEx(self.handle, c_uint(nIP), c_uint(nSubNetMask), c_uint(nDefaultGateWay))
    
    # IP configuration method
    def MV_GIGE_SetIpConfig(self, nType):
        MvCamCtrldll.MV_GIGE_SetIpConfig.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetIpConfig.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetIpConfig(self.handle, c_uint(nType))

    # Set transmission type,Unicast or Multicast
    def MV_GIGE_SetTransmissionType(self, stTransmissionType):
        MvCamCtrldll.MV_GIGE_SetTransmissionType.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_SetTransmissionType.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetTransmissionType(self.handle, byref(stTransmissionType))

    # Save image, support Bmp and Jpeg.
    def MV_CC_SaveImageEx2(self, stSaveParam):
        MvCamCtrldll.MV_CC_SaveImageEx2.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SaveImageEx2.restype = c_uint
        return MvCamCtrldll.MV_CC_SaveImageEx2(self.handle, byref(stSaveParam))

    # Pixel format conversion
    def MV_CC_ConvertPixelType(self, stConvertParam):
        MvCamCtrldll.MV_CC_ConvertPixelType.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_ConvertPixelType.restype = c_uint
        return MvCamCtrldll.MV_CC_ConvertPixelType(self.handle, byref(stConvertParam))

    # Save camera feature
    def MV_CC_FeatureSave(self, pFileName):
        MvCamCtrldll.MV_CC_FeatureSave.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FeatureSave.restype = c_uint
        return MvCamCtrldll.MV_CC_FeatureSave(self.handle, pFileName.encode('ascii'))
    
    # Load camera feature
    def MV_CC_FeatureLoad(self, pFileName):
        MvCamCtrldll.MV_CC_FeatureLoad.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FeatureLoad.restype = c_uint
        return MvCamCtrldll.MV_CC_FeatureLoad(self.handle, pFileName.encode('ascii'))

    # Read the file from the camera
    def MV_CC_FileAccessRead(self, stFileAccess):
        MvCamCtrldll.MV_CC_FileAccessRead.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FileAccessRead.restype = c_uint
        return MvCamCtrldll.MV_CC_FileAccessRead(self.handle, byref(stFileAccess))

    # Write the file to camera
    def MV_CC_FileAccessWrite(self, stFileAccess):
        MvCamCtrldll.MV_CC_FileAccessWrite.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FileAccessWrite.restype = c_uint
        return MvCamCtrldll.MV_CC_FileAccessWrite(self.handle, byref(stFileAccess))

    # Get File Access Progress
    def MV_CC_GetFileAccessProgress(self, stFileAccessProgress):
        MvCamCtrldll.MV_CC_GetFileAccessProgress.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetFileAccessProgress.restype = c_uint
        return MvCamCtrldll.MV_CC_GetFileAccessProgress(self.handle, byref(stFileAccessProgress))

    # Get the optimal Packet Size, Only support GigE Camera
    def MV_CC_GetOptimalPacketSize(self):
        MvCamCtrldll.MV_CC_GetOptimalPacketSize.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_GetOptimalPacketSize.restype = c_uint
        return MvCamCtrldll.MV_CC_GetOptimalPacketSize(self.handle)

    # Start Record
    def MV_CC_StartRecord(self, stRecordParam):
        MvCamCtrldll.MV_CC_StartRecord.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_StartRecord.restype = c_uint
        return MvCamCtrldll.MV_CC_StartRecord(self.handle, byref(stRecordParam))

    # Input RAW data to Record
    def MV_CC_InputOneFrame(self, stInputFrameInfo):
        MvCamCtrldll.MV_CC_InputOneFrame.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_InputOneFrame.restype = c_uint
        return MvCamCtrldll.MV_CC_InputOneFrame(self.handle, byref(stInputFrameInfo))

    #Stop Record
    def MV_CC_StopRecord(self):
        MvCamCtrldll.MV_CC_StopRecord.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_StopRecord.restype = c_uint
        return MvCamCtrldll.MV_CC_StopRecord(self.handle)

    #Get SDK Version
    def MV_CC_GetSDKVersion(self):
        MvCamCtrldll.MV_CC_GetSDKVersion.restype = c_uint
        return MvCamCtrldll.MV_CC_GetSDKVersion()
    
    #Get supported Transport Layer
    def MV_CC_EnumerateTls(self):
        MvCamCtrldll.MV_CC_EnumerateTls.restype = c_uint
        return MvCamCtrldll.MV_CC_EnumerateTls()

    #Enumerate device according to manufacture name
    @staticmethod
    def MV_CC_EnumDevicesEx(nTLayerType, stDevList, strManufacturerName):
        MvCamCtrldll.MV_CC_EnumDevicesEx.argtype = (c_uint, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_EnumDevicesEx.restype = c_uint
        return MvCamCtrldll.MV_CC_EnumDevicesEx(c_uint(nTLayerType), byref(stDevList), byref(strManufacturerName))

    #Is the device accessible
    def MV_CC_IsDeviceAccessible(self, stDevInfo, nAccessMode):
        MvCamCtrldll.MV_CC_IsDeviceAccessible.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_IsDeviceAccessible.restype = c_uint
        return MvCamCtrldll.MV_CC_IsDeviceAccessible(byref(stDevInfo), c_uint(nAccessMode))

    #Set SDK log path
    def MV_CC_SetSDKLogPath(self, strSDKLogPath):
        MvCamCtrldll.MV_CC_SetSDKLogPath.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_SetSDKLogPath.restype = c_uint
        return MvCamCtrldll.MV_CC_SetSDKLogPath(strSDKLogPath.encode('ascii'))

    # Is The Device Connected
    def MV_CC_IsDeviceConnected(self):
        MvCamCtrldll.MV_CC_IsDeviceConnected.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_IsDeviceConnected.restype = c_bool
        return MvCamCtrldll.MV_CC_IsDeviceConnected(self.handle)

    #Register the image callback function
    def MV_CC_RegisterImageCallBackForRGB(self, CallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterImageCallBackForRGB.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterImageCallBackForRGB.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterImageCallBackForRGB(self.handle, CallBackFun, pUser)

    #Register the image callback function
    def MV_CC_RegisterImageCallBackForBGR(self, CallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterImageCallBackForBGR.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterImageCallBackForBGR.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterImageCallBackForBGR(self.handle, CallBackFun, pUser)

    #Get one frame of RGB data, this function is using query to get data query whether the internal cache has data, get data if there has, return error code if no data
    def MV_CC_GetImageForRGB(self, pData, nDataSize, stFrameInfo, nMsec):
        MvCamCtrldll.MV_CC_GetImageForRGB.argtype = (c_void_p, c_void_p, c_uint, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetImageForRGB.restype = c_uint
        # C原型:int MV_CC_GetImageForRGB(IN void* handle, IN OUT unsigned char * pData , IN unsigned int nDataSize, IN OUT MV_FRAME_OUT_INFO_EX* pstFrameInfo, int nMsec);
        return MvCamCtrldll.MV_CC_GetImageForRGB(self.handle, pData, nDataSize, byref(stFrameInfo), c_uint(nMsec))
    
    #Get one frame of BGR data, this function is using query to get data query whether the internal cache has data, get data if there has, return error code if no data
    def MV_CC_GetImageForBGR(self, pData, nDataSize, stFrameInfo, nMsec):
        MvCamCtrldll.MV_CC_GetImageForBGR.argtype = (c_void_p, c_void_p, c_uint, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetImageForBGR.restype = c_uint
        return MvCamCtrldll.MV_CC_GetImageForBGR(self.handle, pData, nDataSize, byref(stFrameInfo), c_uint(nMsec))

    #Get a frame of an image using an internal cache(Cannot be used together with the interface of MV_CC_Display)
    def MV_CC_GetImageBuffer(self, pstFrame, nMsec):
        MvCamCtrldll.MV_CC_GetImageBuffer.argtype = (c_void_p, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetImageBuffer.restype = c_uint
        return MvCamCtrldll.MV_CC_GetImageBuffer(self.handle, byref(pstFrame), c_uint(nMsec))

    #Get a frame of an image using an internal cache(Cannot be used together with the interface of MV_CC_Display)
    def MV_CC_FreeImageBuffer(self, stFrameInfo):
        MvCamCtrldll.MV_CC_FreeImageBuffer.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FreeImageBuffer.restype = c_uint
        return MvCamCtrldll.MV_CC_FreeImageBuffer(self.handle, byref(stFrameInfo))
    
    #if Image buffers has retrieved the data，Clear them
    def MV_CC_ClearImageBuffer(self):
        MvCamCtrldll.MV_CC_ClearImageBuffer.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_ClearImageBuffer.restype = c_uint
        return MvCamCtrldll.MV_CC_ClearImageBuffer(self.handle)

    #Get a frame of an image using an internal cache(Cannot be used together with the interface of MV_CC_Display)
    def MV_CC_DisplayOneFrame(self, pstDisplayInfo):
        MvCamCtrldll.MV_CC_DisplayOneFrame.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_DisplayOneFrame.restype = c_uint
        return MvCamCtrldll.MV_CC_DisplayOneFrame(self.handle, byref(pstDisplayInfo))

    #Set the number of the internal image cache nodes in SDK, Greater than or equal to 1, to be called before the capture
    def MV_CC_SetImageNodeNum(self, nNum):
        MvCamCtrldll.MV_CC_SetImageNodeNum.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetImageNodeNum.restype = c_uint
        return MvCamCtrldll.MV_CC_SetImageNodeNum(self.handle, c_uint(nNum))

    #Set Grab Strategy
    def MV_CC_SetGrabStrategy(self, enGrabStrategy):
        MvCamCtrldll.MV_CC_SetGrabStrategy.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetGrabStrategy.restype = c_uint
        return MvCamCtrldll.MV_CC_SetGrabStrategy(self.handle, c_uint(enGrabStrategy))

    #Set The Size of Output Queue(Only work under the strategy of MV_GrabStrategy_LatestImages，rang：1-ImageNodeNum)
    def MV_CC_SetOutputQueueSize(self, nOutputQueueSize):
        MvCamCtrldll.MV_CC_SetOutputQueueSize.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetOutputQueueSize.restype = c_uint
        return MvCamCtrldll.MV_CC_SetOutputQueueSize(self.handle, c_uint(nOutputQueueSize))

    #Get device information
    def MV_CC_GetDeviceInfo(self, pstDevInfo):
        MvCamCtrldll.MV_CC_GetDeviceInfo.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetDeviceInfo.restype = c_uint
        return MvCamCtrldll.MV_CC_GetDeviceInfo(self.handle, byref(pstDevInfo))

    #Get various type of information
    def MV_CC_GetAllMatchInfo(self, pstInfo):
        MvCamCtrldll.MV_CC_GetAllMatchInfo.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetAllMatchInfo.restype = c_uint
        return MvCamCtrldll.MV_CC_GetAllMatchInfo(self.handle, byref(pstInfo))

    #Get Integer value
    def MV_CC_GetIntValueEx(self, strKey, pstIntValue):
        MvCamCtrldll.MV_CC_GetIntValueEx.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetIntValueEx.restype = c_uint
        return MvCamCtrldll.MV_CC_GetIntValueEx(self.handle, byref(strKey), byref(pstIntValue))
    
    #Set Integer value
    def MV_CC_SetIntValueEx(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetIntValueEx.argtype = (c_void_p, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetIntValueEx.restype = c_uint
        return MvCamCtrldll.MV_CC_SetIntValueEx(self.handle, strKey.encode('ascii'), c_uint(nValue))
    
    #Set Enum value
    def MV_CC_SetEnumValueByString(self, strKey, sValue):
        MvCamCtrldll.MV_CC_SetEnumValueByString.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetEnumValueByString.restype = c_uint
        return MvCamCtrldll.MV_CC_SetEnumValueByString(self.handle, strKey.encode('ascii'), sValue.encode('ascii'))

    #Invalidate GenICam Nodes
    def MV_CC_InvalidateNodes(self):
        MvCamCtrldll.MV_CC_InvalidateNodes.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_InvalidateNodes.restype = c_uint
        return MvCamCtrldll.MV_CC_InvalidateNodes(self.handle)
    
    #Device Local Upgrade
    def MV_CC_LocalUpgrade(self, strFilePathName):
        MvCamCtrldll.MV_CC_LocalUpgrade.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_LocalUpgrade.restype = c_uint
        return MvCamCtrldll.MV_CC_LocalUpgrade(self.handle, strFilePathName.encode('ascii'))

    #Device Local Upgrade
    def MV_CC_GetUpgradeProcess(self, pnProcess):
        MvCamCtrldll.MV_CC_GetUpgradeProcess.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetUpgradeProcess.restype = c_uint
        return MvCamCtrldll.MV_CC_GetUpgradeProcess(self.handle, byref(pnProcess))

    #Read Memory
    def MV_CC_ReadMemory(self, pBuffer, nAddress, nLength):
        MvCamCtrldll.MV_CC_ReadMemory.argtype = (c_void_p, c_void_p, c_uint, c_uint)
        MvCamCtrldll.MV_CC_ReadMemory.restype = c_uint
        return MvCamCtrldll.MV_CC_ReadMemory(self.handle, pBuffer, c_uint(nAddress), c_uint(nLength))

    #Write Memory
    def MV_CC_WriteMemory(self, pBuffer, nAddress, nLength):
        MvCamCtrldll.MV_CC_WriteMemory.argtype = (c_void_p, c_void_p, c_uint, c_uint)
        MvCamCtrldll.MV_CC_WriteMemory.restype = c_uint
        return MvCamCtrldll.MV_CC_WriteMemory(self.handle, pBuffer, c_uint(nAddress), c_uint(nLength))

    #Register event callback, which is called after the device is opened
    def MV_CC_RegisterAllEventCallBack(self, EventCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterAllEventCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterAllEventCallBack.restype = c_uint
        return MvCamCtrldll.MV_CC_RegisterAllEventCallBack(self.handle, EventCallBackFun, pUser)

    # ch:设置仅使用某种模式,type: MV_NET_TRANS_x，不设置时，默认优先使用driver | en: Set to use only one mode,type: MV_NET_TRANS_x. When do not set, priority is to use driver by default
    def MV_GIGE_SetNetTransMode(self, nType):
        MvCamCtrldll.MV_GIGE_SetNetTransMode.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetNetTransMode.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetNetTransMode(self.handle, c_uint(nType))

    #Get net transmission information
    def MV_GIGE_GetNetTransInfo(self, pstInfo):
        MvCamCtrldll.MV_GIGE_GetNetTransInfo.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetNetTransInfo.restype = c_uint
        return MvCamCtrldll.MV_GIGE_GetNetTransInfo(self.handle, byref(pstInfo))

    #Set GVCP cammand timeout
    def MV_GIGE_SetGvcpTimeout(self, nMillisec):
        MvCamCtrldll.MV_GIGE_SetGvcpTimeout.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetGvcpTimeout.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetGvcpTimeout(self.handle, c_uint(nMillisec))

    #Get GVCP cammand timeout
    def MV_GIGE_GetGvcpTimeout(self, pnMillisec):
        MvCamCtrldll.MV_GIGE_GetGvcpTimeout.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetGvcpTimeout.restype = c_uint
        return MvCamCtrldll.MV_GIGE_GetGvcpTimeout(self.handle, byref(pnMillisec))

    #Set the number of retry GVCP cammand
    def MV_GIGE_SetRetryGvcpTimes(self, nRetryGvcpTimes):
        MvCamCtrldll.MV_GIGE_SetRetryGvcpTimes.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetRetryGvcpTimes.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetRetryGvcpTimes(self.handle, c_uint(nRetryGvcpTimes))

    #Get GVCP cammand timeout
    def MV_GIGE_GetRetryGvcpTimes(self, pnRetryGvcpTimes):
        MvCamCtrldll.MV_GIGE_GetRetryGvcpTimes.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetRetryGvcpTimes.restype = c_uint
        return MvCamCtrldll.MV_GIGE_GetRetryGvcpTimes(self.handle, byref(pnRetryGvcpTimes))

    #Set whethe to enable resend, and set resend
    def MV_GIGE_SetResend(self, bEnable,nMaxResendPercent=10,nResendTimeout=50):
        MvCamCtrldll.MV_GIGE_SetResend.argtype = (c_void_p, c_uint, c_uint, c_uint)
        MvCamCtrldll.MV_GIGE_SetResend.restype = c_uint
        return MvCamCtrldll.MV_GIGE_SetResend(self.handle, c_uint(bEnable), c_uint(nMaxResendPercent),c_uint(nResendTimeout))

    #Issue Action Command
    def MV_GIGE_IssueActionCommand(self, pstActionCmdInfo, pstActionCmdResults):
        MvCamCtrldll.MV_GIGE_IssueActionCommand.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_IssueActionCommand.restype = c_uint
        return MvCamCtrldll.MV_GIGE_IssueActionCommand(byref(pstActionCmdInfo, byref(pstActionCmdResults)))

    #Get Multicast Status
    def MV_GIGE_GetMulticastStatus(self, pstDevInfo, pbStatus):
        MvCamCtrldll.MV_GIGE_GetMulticastStatus.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetMulticastStatus.restype = c_uint
        return MvCamCtrldll.MV_GIGE_GetMulticastStatus(byref(pstDevInfo, byref(pbStatus)))

    #Set device bauderate using one of the CL_BAUDRATE_XXXX value
    def MV_CAML_SetDeviceBauderate(self, nBaudrate):
        MvCamCtrldll.MV_CAML_SetDeviceBauderate.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CAML_SetDeviceBauderate.restype = c_uint
        return MvCamCtrldll.MV_CAML_SetDeviceBauderate(self.handle, c_uint(nBaudrate))

    #Returns the current device bauderate, using one of the CL_BAUDRATE_XXXX value
    def MV_CAML_GetDeviceBauderate(self, pnCurrentBaudrate):
        MvCamCtrldll.MV_CAML_GetDeviceBauderate.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CAML_GetDeviceBauderate.restype = c_uint
        return MvCamCtrldll.MV_CAML_GetDeviceBauderate(self.handle, byref(pnCurrentBaudrate))

    #Returns supported bauderates of the combined device and host interface
    def MV_CAML_GetSupportBauderates(self, pnBaudrateAblity):
        MvCamCtrldll.MV_CAML_GetSupportBauderates.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CAML_GetSupportBauderates.restype = c_uint
        return MvCamCtrldll.MV_CAML_GetSupportBauderates(self.handle, byref(pnBaudrateAblity))
    
    #Sets the timeout for operations on the serial port
    def MV_CAML_SetGenCPTimeOut(self, nMillisec):
        MvCamCtrldll.MV_CAML_SetGenCPTimeOut.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CAML_SetGenCPTimeOut.restype = c_uint
        return MvCamCtrldll.MV_CAML_SetGenCPTimeOut(self.handle, c_uint(nMillisec))

    #Set transfer size of U3V device
    def MV_USB_SetTransferSize(self, nTransferSize):
        MvCamCtrldll.MV_USB_SetTransferSize.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_USB_SetTransferSize.restype = c_uint
        return MvCamCtrldll.MV_USB_SetTransferSize(self.handle, c_uint(nTransferSize))

    #Get transfer size of U3V device
    def MV_USB_GetTransferSize(self, pnTransferSize):
        MvCamCtrldll.MV_USB_GetTransferSize.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_USB_GetTransferSize.restype = c_uint
        return MvCamCtrldll.MV_USB_GetTransferSize(self.handle, byref(pnTransferSize))

    #Set transfer ways of U3V device
    def MV_USB_SetTransferWays(self, nTransferWays):
        MvCamCtrldll.MV_USB_SetTransferWays.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_USB_SetTransferWays.restype = c_uint
        return MvCamCtrldll.MV_USB_SetTransferWays(self.handle, c_uint(nTransferWays))

    #Get transfer ways of U3V device
    def MV_USB_GetTransferWays(self, pnTransferWays):
        MvCamCtrldll.MV_USB_GetTransferWays.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_USB_GetTransferWays.restype = c_uint
        return MvCamCtrldll.MV_USB_GetTransferWays(self.handle, byref(pnTransferWays))

    #Enumerate Interfaces with GenTL
    def MV_CC_EnumInterfacesByGenTL(self, pstIFList, strGenTLPath):
        MvCamCtrldll.MV_CC_EnumInterfacesByGenTL.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_EnumInterfacesByGenTL.restype = c_uint
        return MvCamCtrldll.MV_CC_EnumInterfacesByGenTL(byref(pstIFList), strGenTLPath.encode('ascii'))
    
    #Enumerate Devices with GenTL interface
    def MV_CC_EnumDevicesByGenTL(self, pstIFInfo, pstDevList):
        MvCamCtrldll.MV_CC_EnumDevicesByGenTL.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_EnumDevicesByGenTL.restype = c_uint
        return MvCamCtrldll.MV_CC_EnumDevicesByGenTL(byref(pstIFInfo), byref(pstDevList))
    
    #Create Device Handle with GenTL Device Info
    def MV_CC_CreateHandleByGenTL(self, pstDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandleByGenTL.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandleByGenTL.restype = c_uint
        return MvCamCtrldll.MV_CC_CreateHandleByGenTL(byref(self.handle), byref(pstDevInfo))

    #Get camera feature tree XML
    def MV_XML_GetGenICamXML(self, pData, nDataSize, pnDataLen):
        MvCamCtrldll.MV_XML_GetGenICamXML.argtype = (c_void_p, c_void_p, c_uint, c_void_p)
        MvCamCtrldll.MV_XML_GetGenICamXML.restype = c_uint
        return MvCamCtrldll.MV_XML_GetGenICamXML(self.handle, byref(pData), c_uint(nDataSize), byref(pnDataLen))

    #Get Access mode of cur node
    def MV_XML_GetNodeAccessMode(self, strName, penAccessMode):
        MvCamCtrldll.MV_XML_GetNodeAccessMode.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_XML_GetNodeAccessMode.restype = c_uint
        return MvCamCtrldll.MV_XML_GetNodeAccessMode(self.handle, strName.encode('ascii'), byref(penAccessMode))

    #Get Interface Type of cur node
    def MV_XML_GetNodeInterfaceType(self, strName, penInterfaceType):
        MvCamCtrldll.MV_XML_GetNodeInterfaceType.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_XML_GetNodeInterfaceType.restype = c_uint
        return MvCamCtrldll.MV_XML_GetNodeInterfaceType(self.handle, strName.encode('ascii'), byref(penInterfaceType))

    #Save the image file
    def MV_CC_SaveImageToFile(self, pstSaveFileParam):
        MvCamCtrldll.MV_CC_SaveImageToFile.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SaveImageToFile.restype = c_uint
        return MvCamCtrldll.MV_CC_SaveImageToFile(self.handle, byref(pstSaveFileParam))

    #Save 3D point data, support PLY、CSV and OBJ
    def MV_CC_SavePointCloudData(self, pstPointDataParam):
        MvCamCtrldll.MV_CC_SavePointCloudData.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SavePointCloudData.restype = c_uint
        return MvCamCtrldll.MV_CC_SavePointCloudData(self.handle, byref(pstPointDataParam))
    
    #Interpolation algorithm type setting
    def MV_CC_SetBayerCvtQuality(self, nBayerCvtQuality):
        MvCamCtrldll.MV_CC_SetBayerCvtQuality.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetBayerCvtQuality.restype = c_uint
        return MvCamCtrldll.MV_CC_SetBayerCvtQuality(self.handle, c_uint(nBayerCvtQuality))