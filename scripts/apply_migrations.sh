unset -v ENV_FILE

while getopts e:n: opt; do
  case $opt in
    e) ENV_FILE=$OPTARG ;;
    *)
      echo 'Error in command line parsing' >&2
      exit 1
  esac
done

shift "$(( OPTIND - 1 ))"

if [ -z "$ENV_FILE" ]  ; then
  echo 'Missing -e or -n' >&2
  exit 1
fi

export ENV_FILE=$ENV_FILE

# Apply the Alembic migration and capture the output
uv run alembic upgrade head 2>&1

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "Alembic migration applied successfully"
  echo "Log of changes:"

else
  echo "Failed to apply Alembic migration! Please check for errors."
  echo "Error log:"

  exit 1
fi
