import os
import json
from binaryninja import PluginCommand
from .annotate import *

PluginCommand.register_for_function(
  "Annotate",
  "Annotate functions with arguments",
  annotate.run_plugin)
