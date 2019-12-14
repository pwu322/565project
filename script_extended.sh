
echo "the selection metric is: $1"
metric_selection=$1

for ((i=0; i<=14; i++))
do
    python3 get_output_extended.py "$i" "$metric_selection"
done
