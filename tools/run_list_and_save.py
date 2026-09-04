import sounddevice as sd
lines = []
lines.append('Default hostapi: ' + str(sd.default.hostapi))
lines.append('Default device: ' + str(sd.default.device))
lines.append('\nDevices:')
for i, dev in enumerate(sd.query_devices()):
    lines.append(f"{i} {dev['name']} in={dev['max_input_channels']} out={dev['max_output_channels']}")
open('tools/devices.txt','w',encoding='utf-8').write('\n'.join(lines))
print('Wrote tools/devices.txt')
