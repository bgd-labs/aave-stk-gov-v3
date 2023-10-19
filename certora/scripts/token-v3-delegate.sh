if [[ "$1" ]]
then
    RULE="--rule $1"
    MSG="--msg \"$1:: $2\""
fi

echo "RULE is ==>" $RULE "<=="

eval \
certoraRun --send_only \
           --fe_version latest \
           certora/conf/token-v3-delegate.conf $RULE $MSG




