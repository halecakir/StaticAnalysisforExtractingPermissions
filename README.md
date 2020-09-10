# Android Permission Extractor

Extracts permission requesting method information.


### Installation

This module requires [Androguard](https://androguard.readthedocs.io/en/latest/) +v3.3.5 to run.

Install the dependencies.

```sh
$ pip3 install -r requirements.txt
```

### Usage

Analyze single file:

```sh
$ python AnalyzePermissions.py input-apk-file output-file
```

Analyze multiple files:

```sh
$ python AnalyzePermissions.py input-apks-dir outputs-dir
```

### Todos
    
