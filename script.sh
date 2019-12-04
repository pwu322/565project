
echo "the paprameter for constrints is: $1"
parameter_resource_constraint=$1

for ((i=0; i<=14; i++))
do
    python3 get_output.py "$i" "$parameter_resource_constraint"
done