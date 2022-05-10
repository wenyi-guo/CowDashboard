
RUM="HostName=CowRumHub.azure-devices.net;DeviceId=3;SharedAccessKey=3G5cWVVE8YSJmWrTPnK9xmUjIRGf1oDMy41obtkOKJQ="
MILK="HostName=CowMilkHub.azure-devices.net;DeviceId=1;SharedAccessKey=gvZV2qRpNcFyrnVMJLpzk4yarEQqxIe2lfnn/YvyWzQ="
WEATHER="HostName=CowWeatherHub.azure-devices.net;DeviceId=2;SharedAccessKey=VdJyp9ONibHfPpudrqqvH7M7qDDfY0RCXeBBnlDJtTs="
COW="HostName=cowhub.azure-devices.net;DeviceId=milk;SharedAccessKey=AvMmflC1Uztl4FZl1ME4cPhJFkBiZWxRM7jvW6n9qNo="
source venv/bin/activate
python3 temp_controller_with_thermostats.py


# python3 cow_simulator.py $COW "rumination" 
# python3 cow_simulator.py $MILK "milk" &
# python3 cow_simulator.py $WEATHER "weather" &