## Documentation

Haply API
https://haply.gitlab.io/Internal/hardware-api-python/index.html
[Source Code](https://gitlab.com/Haply/public/python_samples)
https://gitlab.com/Haply/2diy/pyhapi
https://gitlab.com/Haply/2diy/pyhapi/-/blob/master/src/HaplyHAPI.py?ref_type=heads

https://haply.gitlab.io/Internal/hardware-api-python/HaplyHardwareAPI.html

The available imports are

- `Device`
- `Handle`
- `Inverse3`
- `SerialStream`
- `UUID`
- `__doc__`
- `__file__`
- `__loader__`
- `__name__`
- `__package__`
- `__spec__`
- `__version__`
- `detect_handles`
- `detect_inverse3s`
- `detect_wired_handles`
- `detect_wireless_handles`
- `get_cpp_version`
- `print_cpp_version`

## Setup

Create a file called ".env" and put add the following information:

```
{
    "port": "COM6", // Enter the string for the device you want to connect to. This likely starts with "COM"
    "debug_mode": false, // Turning this on will use more resources but display extra information, make sure it is off when demoing
}

```

This file is not added to the repository since it is unique to each physical machine.
