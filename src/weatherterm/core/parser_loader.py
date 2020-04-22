import os
import re
import inspect

def _get_parser_list(dirname):
    files = [
        f.replace('.py', '')
        for f in
            os.listdir(dirname)
            if not f.startswith('__')
        ]

    return files

def _import_parsers(parserfiles):    
    m = re.compile('.+parser$', re.I)

    _modules = __import__('weatherterm.parsers', 
        globals(), locals(), parserfiles, 0)

    _parsers = [
        (name, p) for name, p in inspect.getmembers(_modules)
        if inspect.ismodule(p) and m.match(name)
        ]

    _classes = dict()
        for name, p in _parsers:
            _classes.update({
                name: p for name, p in inspect.getmembers(p)
                if inspect.isclass(p) and m.match(name)
            })
    
    return _classes

def load(dirname):
    parserfiles = _get_parser_list(dirname)

    return _import_parsers(parserfiles)