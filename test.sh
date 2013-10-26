#!/bin/bash

echo -e "\n>>> python client test <<<\n\n"
# setting pythonpath to enable python client module loading
export PYTHONPATH="$PYTHONPATH:`pwd`/client/python"
nosetests --nocapture client/python
py_status=$?

echo -e "\n\n\n>>> php client test <<<\n"
cd client/php && phpunit && cd ../..
php_status=$?

# return error exit status code if any of tests have failed
status=$(($py_status + $php_status))
exit $status
