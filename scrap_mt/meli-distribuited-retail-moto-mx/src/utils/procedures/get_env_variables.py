import os

def get_env_variables(prefix):
    return {
        'database': os.getenv(f'DATABASE_{prefix}'),
        'password': os.getenv(f'PASSWORD_{prefix}'),
        'user': os.getenv(f'USER_{prefix}'),
        'host': os.getenv(f'HOST_{prefix}'),
    }