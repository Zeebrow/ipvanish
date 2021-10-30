# what do I want this project to look like?

## target workflow

```
$ pip install ipvanish
$ ipvanish --help
ipvanish [OPTS[, OPTOPTS]]
```

```
$ ipvanish --list-countries
Found 69 countries:
AS  BE  CR  DI  ... US
```

```
$ ipvanish --list-servers --country=US --city=Atl # should be able to find this
Found 69 servers in 'Atlanta (US)':
US-atl-a01: (120 ms)
US-atl-a02: (32 ms)
...
US-atl-a69: (420 ms)
```

```
$ ipvanish --find-best --country=US --city=Atl
US-atl-a02: (32 ms)
US-atl-a01: (120 ms)
...
US-atl-a69: (420 ms)
```
