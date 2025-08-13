# pyscript-api
service that enables customers to execute arbitrary python code on a cloud server. The user sends a python script and the execution result of the main() function gets returned.

# example command to run python script
curl -X POST -F "file=@/Users/hamzahahmadi/Downloads/test.py" http://localhost:8080/execute
or simply
curl -X POST -F "file=@~/Downloads/test.py" http://localhost:8080/execute

# example python script (test.py)
import numpy as np
import pandas as pd

def main():
    # Print something to stdout
    print("Hello from stdout!", flush=True)

    # Create a sample numpy array
    arr = np.array([1, 2, 3, 4, 5])
    print("Numpy array:", arr, flush=True)

    # Create a simple pandas DataFrame
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 22]
    })
    print("DataFrame:\n", df, flush=True)

    # Return the DataFrame as a dictionary
    return df.to_dict()

#Optional: allow running without calling main explicitly
if __name__ == "__main__":
    main()

# return

{
“result”: ..., # return of the main() function
“stdout”: ... # the stdout of the script execution
}

i.e

{"result":{"Age":{"0":25,"1":30,"2":22},"Name":{"0":"Alice","1":"Bob","2":"Charlie"}},"stdout":""}

# no main()

{"error":"Uploaded script does not define a main() function"}



