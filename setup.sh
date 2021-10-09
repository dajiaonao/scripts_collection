#setup the scripts
# echo `dirname $(realpath $0)`
export SC_PATH=`dirname $(realpath $0)`

# ### bin: ttl slideReport
export PATH=$SC_PATH/sh_scripts:$PATH
# 
# ### python path
export PYTHONPATH=$SC_PATH/py_scripts:$PYTHONPATH
# 
# ### ROOT macros: ttreelook, myPhi, savecanvas
echo "add \$SC_PATH/root_scripts to your ~/.rootrc"
