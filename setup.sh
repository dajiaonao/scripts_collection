#setup the scripts
# echo `dirname $(realpath $0)`
export SC_PATH=`dirname $(realpath $0)`

# ### bin: ttl slideReport
export PATH=$SC_PATH/sh_scripts:$PATH

## add slides_report
if [ -f $SC_PATH/sh_scripts/slides_report ]; then
	ln -s $SC_PATH/sh_scripts/slidesReport.py $SC_PATH/sh_scripts/slides_report
fi

## add check_overlap
if [ -f $SC_PATH/sh_scripts/check_overlap ]; then
	ln -s $SC_PATH/sh_scripts/checkOverlap.py $SC_PATH/sh_scripts/check_overlap
fi

# ### python path
export PYTHONPATH=$SC_PATH/py_scripts:$PYTHONPATH
# 
# ### ROOT macros: ttreelook, myPhi, savecanvas
echo "add \$SC_PATH/root_scripts to your ~/.rootrc"
