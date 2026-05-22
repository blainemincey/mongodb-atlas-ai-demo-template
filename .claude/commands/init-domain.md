Initialize the Atlas AI demo with a domain pack from the `domains/` directory.

If no domain name was given as an argument (`$ARGUMENTS`), run:

```
python scripts/init_domain.py --list
```

Print the available domains and ask the user which one to apply. Wait for their response before proceeding.

If a domain name was given, run:

```
python scripts/init_domain.py $ARGUMENTS
```

After the script completes, report:
1. Which files were copied or patched (from the script output)
2. The next steps printed by the script (env vars needed, setup.py, start.sh)

If the script exits with an error, show the error message and stop — do not attempt to fix it automatically.
