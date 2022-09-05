from enum import Enum, auto
from pyvesc.messages.base import VESCMessage
from datatypes import *

class ZeroEnum(Enum):
    def _generate_next_value_(name,start,count,last_values):
        return count

class ControllerCommands(ZeroEnum):
    COMM_FW_VERSION = auto()
    COMM_GET_AUXVALUES = auto()
    COMM_GET_CONTROLSTATE = auto()
    COMM_GET_ALLCONTROLSTATE = auto()
    COMM_GET_SETPOINTS = auto()
    COMM_SET_POWER = auto()
    COMM_SET_DUTY_CYCLE = auto()
    COMM_SET_SETPOINTS = auto()
    COMM_START_SAMPLING = auto()
    COMM_STOP_SAMPLING = auto()
    COMM_PRINT = auto()
    COMM_ZERO_ADC = auto()
    COMM_REBOOT = auto()
    COMM_ALIVE = auto()
    COMM_GET_LAST_EVENTS = auto()
    COMM_ERASE_LOG = auto()
    COMM_APPEND_TO_LOG = auto()
    COMM_RESET_OVERVOLTAGE = auto()
    COMM_RESET_SAFETY = auto()
    COMM_TOGGLE_CAPREALVOLTAGE = auto()
    COMM_JUMP_TO_BOOTLOADER = 22
    COMM_ERASE_NEW_FW = auto()
    COMM_WRITE_NEW_FW_DATA = auto()
    COMM_GET_STATUS = auto()
    COMM_INVALID_PACKAGE = auto()
    COMM_GET_ALLCONTROLSIZE = auto()
    COMM_OPEN_BRIDGERELAY = auto()
    COMM_CLOSE_BRIDGERELAY = auto()
    COMM_STOP_RUNNING = auto()
    COMM_SET_CALIBRATION = auto()
    COMM_GET_CALIBRATION = auto()
    COMM_SENDGET_ALLCONTROLSTATE = auto()
    COMM_STOPANDRESET = auto()
    COMM_GET_GENERATORSTATE = auto()
    COMM_GET_ISNEWSAMPLEDEVENT = auto()
    COMM_SET_FBR = auto()
    COMM_SET_STOPSAMPLINGONTHISEVENT = auto()

class GetAuxValues(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_AUXVALUES.value
    fields = auxFields

class GetControlState(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_CONTROLSTATE.value
    fields = controlFields + sysInputFields

class GetAllControlSize(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_ALLCONTROLSIZE.value
    fields = [('amount','h',1)]

class SetOpenBridgeRelay(metaclass=VESCMessage):
    id = ControllerCommands.COMM_OPEN_BRIDGERELAY.value
    fields = []

class SetCloseBridgeRelay(metaclass=VESCMessage):
    id = ControllerCommands.COMM_CLOSE_BRIDGERELAY.value
    fields = []

class StopRunning(metaclass=VESCMessage):
    id = ControllerCommands.COMM_STOP_RUNNING.value
    fields = []

class GetAllControlState(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_ALLCONTROLSTATE.value
    fields = [('count','h',100)] + controlFields + sysInputFields

class sendGetAllControlState(metaclass=VESCMessage):
    id = ControllerCommands.COMM_SENDGET_ALLCONTROLSTATE.value
    fields = [('count','h',1)]

class GetSetPoints(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_SETPOINTS.value
    fields = setPointsFields

class SetSetPoints(metaclass=VESCMessage):
    id = ControllerCommands.COMM_SET_SETPOINTS.value
    fields = setPointsFields

class ResetController(metaclass=VESCMessage):
    id = ControllerCommands.COMM_REBOOT.value
    fields = []

class SetDutyCycle(metaclass=VESCMessage):
    id = ControllerCommands.COMM_SET_DUTY_CYCLE.value
    fields = [('dutyCycle','i',100)]

class StartSampling(metaclass=VESCMessage):
    id = ControllerCommands.COMM_START_SAMPLING.value
    fields = [('divider','i',1)]

class StopSampling(metaclass=VESCMessage):
    id = ControllerCommands.COMM_STOP_SAMPLING.value
    fields = []

class Print(metaclass=VESCMessage):
    id = ControllerCommands.COMM_PRINT.value
    fields = [('text','s',1)]

class GetLastEvents(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_LAST_EVENTS.value
    fields = [('events','i',1)]

class ResetLog(metaclass=VESCMessage):
    id = ControllerCommands.COMM_ERASE_LOG.value
    fields = []

class ResetOvervoltage(metaclass=VESCMessage):
    id = ControllerCommands.COMM_RESET_OVERVOLTAGE.value
    fields = []

class ResetSafety(metaclass=VESCMessage):
    id = ControllerCommands.COMM_RESET_SAFETY.value
    fields = []

class ToggleCapRealVoltage(metaclass=VESCMessage):
    id = ControllerCommands.COMM_TOGGLE_CAPREALVOLTAGE.value
    fields = []

class AppendToLog(metaclass=VESCMessage):
    id = ControllerCommands.COMM_APPEND_TO_LOG.value
    fields = []

class GetStatus(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_STATUS.value
    fields = statusFields

class GetGenerator(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_GENERATORSTATE.value
    fields = generatorFields

class GetIsNewEvent(metaclass=VESCMessage):
    id = ControllerCommands.COMM_GET_ISNEWSAMPLEDEVENT.value
    fields = [('isNewEvent','B',1)]

class SetStopSamplingEvent(metaclass=VESCMessage):
    id = ControllerCommands.COMM_SET_STOPSAMPLINGONTHISEVENT.value
    fields = [('event','i',1)]