unset -v ENV_FILE
unset -v NAME
unset -v SCHEMA

while getopts e:n:s: opt; do
  case $opt in
    e) ENV_FILE=$OPTARG ;;
    n) NAME=$OPTARG ;;
    s) SCHEMA=$OPTARG ;;
    *)
      echo 'Error in command line parsing' >&2
      exit 1
  esac
done

shift "$(( OPTIND - 1 ))"

if [ -z "$ENV_FILE" ] || [ -z "$NAME" ] || [ -z "$SCHEMA" ]; then
  echo 'Missing -e or -n or -s' >&2
  exit 1
fi

export ENV_FILE=$ENV_FILE
export SCHEMA=$SCHEMA

# Run the Alembic revision command with the provided name and capture the output
uv run alembic revision --autogenerate -m "$NAME" 2>&1 && uv run blue .


# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "Alembic migration generated successfully: $NAME"
  echo "Log of changes:"

else
  echo "Failed to create Alembic revision. Please check for errors."
  echo "Error log:"

  exit 1
fi
