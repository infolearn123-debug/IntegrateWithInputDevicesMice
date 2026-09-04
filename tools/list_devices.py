import sounddevice as sd

print('Default hostapi:', sd.default.hostapi)
print('Default device:', sd.default.device)
print('\nDevices:')
for i, dev in enumerate(sd.query_devices()):
    print(i, dev['name'], 'in=', dev['max_input_channels'], 'out=', dev['max_output_channels'])
