import json
import re
import os
from binaryninja import *
import sys 
from .stacks import linux_x86, linux_x64, windows_x86, windows_x64

python2=False
if sys.version_info[0] < 3:
   python2=True

PLUGINDIR_PATH = os.path.abspath(os.path.dirname(__file__))

call_llil = [
  LowLevelILOperation.LLIL_CALL,
  LowLevelILOperation.LLIL_CALL_STACK_ADJUST,
]

reg_arch=["armv7","armv7e","aarch64"]
stack_arch=["x86","x86_64"]

os_sys=""
modules={}
generic={}

def search_files(directory='.', extension=''):
    filenames=[]
    extension = extension.lower()
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            if extension and name.lower().endswith(extension):
                filenames.append(name[:-len(extension)-1])
            elif not extension:
                filenames.append(name)
    return filenames
                
def load_functions(platform):
    global modules
    global generic
    jsonpath=os.path.join(PLUGINDIR_PATH,"data",platform)
    filenames=search_files(jsonpath,"json")
    for module_name in filenames:
        function_file = open(os.path.join(jsonpath,module_name+".json"), 'r')
        function_list = json.load(function_file)
        function_file.close()
        if (platform=="generic"):
            generic[module_name]=function_list #module_name=Function and function_list=arguments for Generic
        else:
            modules[module_name]=function_list

def get_function_name(callee):
  global os_sys
  if os_sys=="windows":
      module_name = re.match('(\S+)\!', callee.name)
      function_name = re.match('\S+\!(\w+)(@IAT)*?', callee.name)
  elif os_sys=="linux":
      if "__imp_" in callee.name:
         function_name=re.match('__imp_(\S+)', callee.name)
      else:
         function_name=re.match('(\S+)', callee.name)
      module_name=re.match('(\S+)', callee.name)
  return (module_name, function_name)

def do_comment(function_arg,stack_args,function):
    global python2
    comment = "<arg: {}>\n".format(function_arg)
    try:
        if python2==True:
            stack_instruction = stack_args.next()
        else:
            stack_instruction = next(stack_args)

        if stack_instruction is None:
            return False

        function.set_comment(stack_instruction.address, function_arg)
        return True
    except StopIteration:
        log_error('[x] Virtual Stack Empty. Unable to find function arguments for <{}>'.format(function_name))
    return False

def func_annotate_stack(module_name, function_name, stack, function):
    global modules
    global generic
    modname=module_name.group(1)
    funcname=function_name.group(1)
    if modname in modules:
        if funcname in modules[modname]:
            stack_args = iter(stack)
            for function_arg in modules[modname][funcname]:
                if (do_comment(function_arg,stack_args,function)==False):
                    break
    else:
        for item in generic:
            if funcname in generic[item]:
                stack_args = iter(stack)
                for function_arg in generic[item][funcname]:
                    if (do_comment(function_arg,stack_args,function)==False):
                        break

def func_annotate_reg(module_name, function_name, instruction, function):
    global modules
    global generic
    modname=module_name.group(1)
    funcname=function_name.group(1)
    mlil=function.medium_level_il
    if modname in modules:
        if funcname in modules[modname]:
            offsets=[]
            params=instruction.medium_level_il.ssa_form.params
            for i in range(0,len(params)):
                if hasattr(params[i], 'constant'): #we do have a constant
                    address=params[i].address
                    offsets.append(address)
                else: 
                    reg=params[i].src
                    try:
                        address=mlil.get_ssa_var_definition(reg).address
                        offsets.append(address)
                    except:
                        pass
            pos=0
            for function_arg in modules[modname][funcname]:
                comment = "<arg: {}>\n".format(function_arg)
                if pos<len(offsets):
                    function.set_comment(offsets[pos], function_arg)
                    pos+=1

    for modname in generic:
        if funcname in generic[modname]:
            offsets=[]
            params=instruction.medium_level_il.ssa_form.params
            if type(params)==list:
                for i in range(0,len(params)):
                    if hasattr(params[i], 'constant'): #we do have a constant
                        address=params[i].address
                        offsets.append(address)
                    else: 
                        reg=params[i].src
                        try:
                            address=mlil.get_ssa_var_definition(reg).address
                            offsets.append(address)
                        except:
                            pass
            pos=0
            for function_arg in generic[modname][funcname]:
                comment = "<arg: {}>\n".format(function_arg)
                if pos<len(offsets):
                    function.set_comment(offsets[pos], function_arg)
                    pos+=1

def run_plugin(bv, function):
    # logic of stack selection
    global os_sys
    global reg_arch
    global stack_arch
    arch=bv.platform.arch.name
    print ("Architecture detected : {architecture}".format(architecture=arch))
    print ("Platform detected: {platform}".format(platform=bv.platform.name))
    if "linux" in bv.platform.name:
        os_sys="linux"
    elif "windows" in bv.platform.name:
        os_sys="windows"
        
    if bv.platform.name == 'linux-x86':
        stack = linux_x86.Stack()
        stack_changing_llil =  stack.get_relevant_llil()
    elif bv.platform.name == 'linux-x86_64':
        stack = linux_x64.Stack()
        stack_changing_llil =  stack.get_relevant_llil()
    elif bv.platform.name == 'windows-x86':
        stack = windows_x86.Stack()
        stack_changing_llil =  stack.get_relevant_llil()
    elif bv.platform.name == 'windows-x86_64':
        stack = windows_x64.Stack()
        stack_changing_llil =  stack.get_relevant_llil()
      
    if os_sys=="windows":
       load_functions("windows")
    elif os_sys=="linux":
       load_functions("linux")
    load_functions("generic")
    
    log_info('[*] Annotating function <{name}>'.format(name=function.symbol.name))
    for block in function.low_level_il:
        for instruction in block:
            if (arch=="x86" or arch=="x86_64"):
                if (instruction.operation in stack_changing_llil):
                    stack.update(instruction)
            if (instruction.operation in call_llil and instruction.dest.operation == LowLevelILOperation.LLIL_CONST_PTR):
                callee = bv.get_function_at(instruction.dest.constant) # Fetching function in question
                if callee!=None:
                    if (callee.symbol.type == SymbolType.ImportedFunctionSymbol):
                        module_and_function = get_function_name(callee)
                        if arch in reg_arch:
                            func_annotate_reg(module_and_function[0], module_and_function[1], instruction, function)
                        elif arch in stack_arch:
                            func_annotate_stack(module_and_function[0], module_and_function[1], stack, function)
            elif (instruction.operation == LowLevelILOperation.LLIL_CALL):
                if (instruction.dest.operation == LowLevelILOperation.LLIL_REG and instruction.dest.value.type == RegisterValueType.ImportedAddressValue):
                    iat_address = instruction.dest.value.value
                    try:
                        callee = bv.get_symbol_at(iat_address)
                        if (callee.type == SymbolType.ImportedFunctionSymbol or callee.type == SymbolType.ImportAddressSymbol):
                            module_and_function = get_function_name(callee)
                            if arch in reg_arch:
                                func_annotate_reg(module_and_function[0], module_and_function[1], instruction, function)
                            elif arch in stack_arch:
                                func_annotate_stack(module_and_function[0], module_and_function[1], stack, function)
                    except AttributeError:
                        continue
                else:
                    try:
                        iat_address = instruction.dest.src.constant
                        callee = bv.get_symbol_at(iat_address)
                        if (callee.type == SymbolType.ImportedFunctionSymbol or callee.type == SymbolType.ImportAddressSymbol):
                            module_and_function = get_function_name(callee)
                            if arch in reg_arch:
                                func_annotate_reg(module_and_function[0], module_and_function[1], instruction, function)
                            elif arch in stack_arch:
                                func_annotate_stack(module_and_function[0], module_and_function[1], stack, function)
                    except AttributeError:
                        continue
