## Documentation

### Processing (py5)

[py5 module](http://py5coding.org/)

### Haply 2DIY

https://haply.gitlab.io/Internal/hardware-api-python/index.html
[Source Code](https://gitlab.com/Haply/public/python_samples)
[Pyhapi repository](https://gitlab.com/Haply/2diy/pyhapi)
[Pyhapi repository - source code](https://gitlab.com/Haply/2diy/pyhapi/-/blob/master/src/HaplyHAPI.py?ref_type=heads)

## Setup

Create a file called ".env" and put add the following information:

```
{
    "port": "COM6", // Enter the string for the device you want to connect to. This likely starts with "COM"
    "debug_mode": false, // Turning this on will use more resources but display extra information, make sure it is off when demoing
}
```

This file is not added to the repository since it is unique to each physical machine.
