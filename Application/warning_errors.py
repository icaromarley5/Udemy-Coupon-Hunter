'''

Module for error management

'''

import os
import codecs

def write_warning(text):
    completeName = os.path.join("", "warnings.txt")
    file_object = codecs.open(completeName, "a", "utf-8")
    file_object.write(text)
