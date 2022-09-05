#Check out all field definitions at https://docs.python.org/3/library/struct.html

auxFields = [  ('temperature', 'i', 10),
                ('vsupply','i',10),
                ('Ipp','i',100),
               ('Rpm','i',100),
               ('Vpp','i',10),
               ('IErr','i',100),
               ('relayState', 'B', 1),
               ('realCapVoltageUsed', 'B', 1),
            ]

generatorFields = [
                    ('lastCycleLength1','i',1),
                    ('lastCycleLength2','i',1),
                    ('lastCycleLength3','i',1),
                    ('lastCycleLength4','i',1),
                    ('lastCycleLength5','i',1),
                    ('lastCycleLength6','i',1),
                    ('lastThreePhaseCycleLength','i',1),
                    ('nextCycleLength','i',1),
                    ('cycleCount','i',1),
                    ('cycleLengthAvg1','i',100000),
                    ('cycleLengthAvg2','i',100000),
                    ('cycleLengthAvg3','i',100000),
                    ('cycleLengthAvg4','i',100000),
                    ('cycleLengthAvg5','i',100000),
                    ('cycleLengthAvg6','i',100000),
                    ('cycleCurrentAvg1','i',100000),
                    ('cycleCurrentAvg2', 'i', 100000),
                    ('cycleCurrentAvg3', 'i', 100000),
                    ('cycleCurrentAvg4', 'i', 100000),
                    ('cycleCurrentAvg5', 'i', 100000),
                    ('cycleCurrentAvg6', 'i', 100000),
                    ('generatorCurrentAvg','i',100000),
                    ]

controlTaskStates = ['idle','Wait Safe relay open','Wait for Current','Charge capacitor','Wait for sync','Running','Simulated running','Stopping','Stopping relayOn','Fixed duty','Overvolt safety','OVSafety RelayOn','Overvolt error','OVError RelayOn','OverTemperature','OVTemp relayOn','Powerloss', 'PWloss, relayOn','Stop and reset', 'StopnRes relayon','bridgemalfunction','bridge mal ron']

controlFields = [('controlTaskState','B',1),
                ('Ucap','i',10),
                ('U12', 'i', 100),
                ('dutyCycle', 'i', 1000),
                ('IErr', 'i', 1000),
                ('UCapErr', 'i', 10),
                ('IOutFiltered', 'i', 100),
                ('IInFiltered', 'i', 100),
                 ]

sysInputFields = [
                ('VCH', 'i', 10),
                ('VIN', 'i', 10),
                ('VOUT', 'i', 10),
                ('IIN', 'i', 100),
                ('IOUT', 'i', 100),
                ('VPH1', 'i', 10),
               ('VPH2', 'i', 10),
                ('VPH3', 'i', 10),
                ]

setPointsFields = [
    ('voltage','i',10),
    ('freq','i',100),
    ('deadTime', 'i', 1),
    ('vbusMin', 'i', 1),
    ('vbusMax', 'i', 1),
    ('iMax', 'i', 10),
]



statusFields = [
    ('temp','i',10),
    ('IErr','i',1000),
    ('IIn','i',100),
    ('UCap','i',10),
    ('controlTaskState', 'B', 1),
    ('lastEvent','B',1),
]


fullControlFields = controlFields + sysInputFields

