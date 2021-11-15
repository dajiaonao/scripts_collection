#setup the scripts
# echo $#
# export SC_PATH=`dirname $(realpath $1)`
export SC_PATH="/public/home/lhcb/scripts/scripts_collection"

# ### bin: ttl slideReport
export PATH=$SC_PATH/sh_scripts:$PATH

## add slides_report
if [ ! -f $SC_PATH/sh_scripts/slides_report ]; then
	ln -s $SC_PATH/py_scripts/slidesReport.py $SC_PATH/sh_scripts/slides_report
fi

## add check_overlap
if [ ! -f $SC_PATH/sh_scripts/check_overlap ]; then
	ln -s $SC_PATH/py_scripts/checkOverlap.py $SC_PATH/sh_scripts/check_overlap
fi

if [ -f /home/lhcb/setups/setup_latex.sh ]; then
	source /home/lhcb/setups/setup_latex.sh
fi

# ### python path
export PYTHONPATH=$SC_PATH/py_scripts:$PYTHONPATH
# 
# ### ROOT macros: ttreelook, myPhi, savecanvas
echo "add \$SC_PATH/root_scripts to your ~/.rootrc"
